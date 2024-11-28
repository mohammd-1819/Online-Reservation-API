from django.db import models
from account.models import User
from reservation.models.reservation import AvailableSlot


class Cart(models.Model):
    user = models.OneToOneField(User, related_name='cart', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    slot = models.ForeignKey(AvailableSlot, related_name='cart_items', on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"reservation for {self.slot.doctor.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    slot = models.ForeignKey(AvailableSlot, on_delete=models.CASCADE, related_name='items')
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.order.user.email
