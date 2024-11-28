from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('account.urls')),
    path('api/reservation/', include('reservation.urls')),
    path('api/cart/', include('cart.urls'))
]
