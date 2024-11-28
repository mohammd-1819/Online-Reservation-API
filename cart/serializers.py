from rest_framework import serializers
from account.models import User
from .models import Cart, CartItem, Order, OrderItem
from reservation.serializers import AvailableSlotSerializer


class CartItemSerializer(serializers.ModelSerializer):
    slot = AvailableSlotSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('slot', 'price', 'quantity')


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Cart
        fields = ('user', 'created_at', 'items')


class OrderItemSerializer(serializers.ModelSerializer):
    slot = AvailableSlotSerializer()

    class Meta:
        model = OrderItem
        exclude = ('order',)


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())
    item = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
