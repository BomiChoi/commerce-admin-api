from django.urls import path

from . import views

urlpatterns = [
    path('', views.OrderListCreateView.as_view()),
    path('/<int:pk>', views.OrderDetailView.as_view()),
]
