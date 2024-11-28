from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from cart.utility.pagination import StandardResultSetPagination
from .serializers import OrderSerializer, CartSerializer
from .models import Cart, Order, OrderItem, CartItem
from reservation.models.reservation import AvailableSlot
import requests
from django.conf import settings

ZARINPAL_REQUEST_URL = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json'
ZARINPAL_VERIFY_URL = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json'
CALLBACK_URL = 'http://localhost:8000/api/payment/verify/'


class CartView(APIView, StandardResultSetPagination):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        doctor_name = request.data.get('doctor_name')
        quantity = int(request.data.get('quantity', 1))

        try:
            slot = AvailableSlot.objects.get(doctor__name=doctor_name, is_booked=False)
        except AvailableSlot.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        price = slot.price

        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, slot=slot)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.price = price * cart_item.quantity
        cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        cart = get_object_or_404(Cart, user=request.user)
        slot = get_object_or_404(AvailableSlot, id=product_id)
        cart_item = get_object_or_404(CartItem, cart=cart, slot=slot)

        cart_item.delete()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({'error': 'No Cart Found'}, status=status.HTTP_400_BAD_REQUEST)

        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        address = request.data.get('address')
        if not address:
            return Response({'detail': 'address is required'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.product.price * item.quantity for item in cart.items.all())
        order = Order.objects.create(user=request.user, total_price=total_price, address=address)

        order_items = []
        for item in cart.items.all():
            order_item = OrderItem(
                order=order,
                slot=item.slot,
                quantity=item.quantity,
                price=item.product.price
            )
            order_items.append(order_item)

        OrderItem.objects.bulk_create(order_items)
        cart.items.all().delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'detail': 'Order Not found'}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.total_price,
            "Description": f"payment {order.id}",
            "CallbackURL": CALLBACK_URL,
        }

        response = requests.post(ZARINPAL_REQUEST_URL, json=data)

        try:
            res_data = response.json()
        except ValueError:
            return Response({'detail': 'Invalid JSON response from server'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if res_data.get('Status') == 100:
            payment_url = f"https://sandbox.zarinpal.com/pg/StartPay/{res_data['Authority']}"
            return Response({'payment_url': payment_url}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Error in request', 'message': res_data.get('Errors')},
                            status=status.HTTP_400_BAD_REQUEST)


class PaymentVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        authority = request.GET.get('Authority')
        status = request.GET.get('Status')

        if status != 'OK':
            return Response({'detail': 'purchase failed.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(user=request.user,
                                      is_paid=False)
        except Order.DoesNotExist:
            return Response({'detail': 'order not found'}, status=status.HTTP_404_NOT_FOUND)

        # confirm payment
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.total_price,
            "Authority": authority,
        }

        response = requests.post(ZARINPAL_VERIFY_URL, json=data)
        res_data = response.json()

        if res_data['Status'] == 100:
            order.is_paid = True
            order.save()
            return Response({'detail': 'purchase successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'purchase failed'}, status=status.HTTP_400_BAD_REQUEST)
