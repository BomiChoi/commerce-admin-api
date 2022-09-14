from rest_framework import serializers

from apps.coupon.models import Coupon, CouponType


class CouponSerializer(serializers.ModelSerializer):
    is_used = serializers.BooleanField(read_only=True)

    class Meta:
        model = Coupon
        fields = (
            'id',
            'type',
            'code',
            'is_used'
        )


class CouponTypeSerializer(serializers.ModelSerializer):
    used_time = serializers.IntegerField(read_only=True)
    total_discount = serializers.DecimalField(max_digits=16, decimal_places=2, read_only=True)

    class Meta:
        model = CouponType
        fields = (
            'id',
            'category',
            'name',
            'value',
            'issue_date',
            'expr_date',
            'used_time',
            'total_discount'
        )
