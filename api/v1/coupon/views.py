from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from apps.coupon.models import Coupon, CouponType
from .serializers import CouponSerializer, CouponTypeSerializer


class CouponListCreateView(ListCreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer


class CouponDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer


class CouponTypeListCreateView(ListCreateAPIView):
    queryset = CouponType.objects.all()
    serializer_class = CouponTypeSerializer


class CouponTypeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CouponType.objects.all()
    serializer_class = CouponTypeSerializer
