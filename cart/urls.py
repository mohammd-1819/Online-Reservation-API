from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('view', views.CartView.as_view(), name='cart-view'),
    path('order/view', views.OrderView.as_view(), name='order-view'),
    path('remove', views.RemoveFromCartView.as_view(), name='cart-remove'),
    path('payment/request/<int:order_id>', views.PaymentRequestView.as_view(), name='payment-request'),
    path('payment/verify/', views.PaymentVerifyView.as_view(), name='payment-verify'),
]


