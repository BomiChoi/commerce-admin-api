from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('/orders', include('api.v1.order.urls')),
    path('/coupons', include('api.v1.coupon.urls')),
    path('/schema', SpectacularAPIView.as_view(), name='schema'),
    path('/swagger', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('/redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
