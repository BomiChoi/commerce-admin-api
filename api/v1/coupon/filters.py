from django_filters import rest_framework as filters

from apps.coupon.models import Coupon, CouponType


class CouponFilter(filters.FilterSet):
    class Meta:
        model = Coupon
        fields = ['is_used', 'type__category']


class CouponTypeFilter(filters.FilterSet):
    class Meta:
        model = CouponType
        fields = ['category']
