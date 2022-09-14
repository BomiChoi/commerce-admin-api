from django.urls import path, include

urlpatterns = [
    path('/orders', include('api.v1.order.urls')),
    path('/coupons', include('api.v1.coupon.urls')),
]
