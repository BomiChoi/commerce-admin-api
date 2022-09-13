from django_filters import rest_framework
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from apps.order.models import Order
from .filters import OrderFilter
from .serializers import OrderSerializer, OrderUpdateSerializer


class OrderListCreateView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = OrderFilter
    search_fields = ['buyr_name']


class OrderDetailView(RetrieveUpdateAPIView):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        """ Retrieve일 때에는 OrderSerializer, Update일 때에는 OrderUpdateSerializer를 반환합니다. """
        if self.request.method == 'GET':
            return OrderSerializer
        else:
            return OrderUpdateSerializer
