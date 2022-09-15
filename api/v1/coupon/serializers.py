from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
            'min_price',
            'used_time',
            'total_discount'
        )

    def validate(self, attrs):
        # 할인값이 100%가 넘지 않는지 확인
        if attrs['category'] == '% 할인' and attrs['value'] > 100:
            raise ValidationError({'value', '할인값은 100%을 넘을 수 없습니다.'})

        # 쿠폰 만료일이 발급일 이후인지 확인
        if 'expr_date' in attrs and attrs['expr_date'] < attrs['issue_date']:
            raise ValidationError({'expr_date', '쿠폰 만료일은 발급일 이후여야 합니다.'})

        return attrs
