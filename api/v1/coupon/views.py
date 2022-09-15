from django_filters import rest_framework
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from apps.coupon.models import Coupon, CouponType
from .filters import CouponFilter, CouponTypeFilter
from .serializers import CouponSerializer, CouponListSerializer, CouponTypeSerializer


class CouponListCreateView(ListCreateAPIView):
    queryset = Coupon.objects.all()
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CouponFilter
    search_fields = ['type__name']

    def get_serializer_class(self):
        """ Create일 때에는 CouponSerializer, List일 때에는 CouponListSerializer를 반환합니다. """

        if self.request.method == 'POST':
            return CouponSerializer
        else:
            return CouponListSerializer


class CouponDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer


class CouponTypeListCreateView(ListCreateAPIView):
    queryset = CouponType.objects.all()
    serializer_class = CouponTypeSerializer
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CouponTypeFilter
    search_fields = ['name']


class CouponTypeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CouponType.objects.all()
    serializer_class = CouponTypeSerializer
