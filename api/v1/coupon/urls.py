from django.urls import path

from . import views

urlpatterns = [
    path('', views.CouponListCreateView.as_view()),
    path('/<int:pk>', views.CouponDetailView.as_view()),
    path('/types', views.CouponTypeListCreateView.as_view()),
    path('/types/<int:pk>', views.CouponTypeDetailView.as_view()),
]
