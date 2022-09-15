import datetime

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.country.models import Country, DeliveryCost
from apps.order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    date = serializers.DateField(read_only=True)
    pay_state = serializers.CharField(read_only=True)
    buyr_country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), write_only=True)
    buyr_country_code = serializers.CharField(source='buyr_country.code', read_only=True)
    vccode = serializers.CharField(source='buyr_country.dcode', read_only=True)
    delivery_cost = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'date',
            'pay_state',
            'quantity',
            'price',
            'buyr_country',
            'buyr_country_code',
            'buyr_city',
            'buyr_zipcode',
            'vccode',
            'delivery_cost',
            'delivery_num',
            'buyr_name',
            'coupon'
        )

    def validate(self, attrs):
        coupon = attrs.get('coupon', None)
        if coupon:
            # 사용 여부 확인
            if coupon.is_used:
                raise ValidationError({'coupon': '이미 사용된 쿠폰입니다.'})

            # 유효기간 확인
            if coupon.type.expr_date and coupon.type.expr_date < datetime.date.today():
                raise ValidationError({'coupon': '사용기간이 만료되었습니다.'})

            # 최소금액조건 확인
            if coupon.type.min_price and float(attrs['price']) < coupon.type.min_price:
                raise ValidationError({'coupon': f'해당 쿠폰은 금액이 {attrs["price"]}원 이상일 때만 사용 가능합니다.'})

            # 할인액이 원래 금액보다 더 크지 않은지 확인
            if coupon.type.category == '정액 할인' and coupon.type.value > attrs['price']:
                raise ValidationError({'coupon': '할인액이 원래 금액보다 더 큽니다.'})

        return attrs

    @transaction.atomic()
    def create(self, validated_data):
        """ 입력받은 주문 정보를 주문일자, 계산된 배송비와 함께 저장 후 반환합니다. """

        # 주문 생성
        order = Order.objects.create(**validated_data)

        # 주문일자 저장
        order.date = datetime.date.today()

        # 국가 설정
        country = order.buyr_country
        is_foreign = (country.code != 'KR')

        # 해외 배송비 책정
        if is_foreign:
            countries = list(set(DeliveryCost.objects.values_list('country__code', flat=True)))
            # 배송비 데이터 없는 국가일 경우 미국 기준으로 책정
            if country.code not in countries:
                country = Country.objects.get(code='US')
            order.delivery_cost = DeliveryCost.objects.get(country=country, quantity=order.quantity).cost

        # 쿠폰 적용
        coupon = validated_data.get('coupon', None)
        if coupon:
            discount_amount = 0
            category = coupon.type.category
            if category == '배송비 할인':
                discount_amount = coupon.type.value
                if discount_amount > order.delivery_cost:
                    raise ValidationError({'coupon': '할인액이 원래 배송비보다 더 큽니다.'})
                order.delivery_cost -= discount_amount
            elif category == '% 할인':
                discount_amount = order.price * coupon.type.value / 100
                order.price -= discount_amount
            elif category == '정액 할인':
                discount_amount = coupon.type.value
                order.price -= discount_amount

            coupon.is_used = True
            coupon.type.used_time += 1
            coupon.type.total_discount += discount_amount
            coupon.save()
            coupon.type.save()

        # 해외일 경우 환율 적용
        if is_foreign:
            rate = 1200  # 달러 환율
            order.price /= rate
            order.delivery_cost /= rate

        # 주문 변경사항 저장 및 반환
        order.save()
        return order


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'pay_state',
        )
