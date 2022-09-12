import datetime

from rest_framework import serializers

from apps.country.models import Country, DeliveryCost
from apps.order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    date = serializers.DateField(read_only=True)
    buyr_country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), write_only=True)
    buyr_country_code = serializers.CharField(source='buyr_country.code', read_only=True)
    vccode = serializers.CharField(source='buyr_country.dcode', read_only=True)
    delivery_cost = serializers.IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'date',
            'pay_state',
            'quantity',
            'price',
            'buyr_city',
            'buyr_country',
            'buyr_country_code',
            'buyr_zipcode',
            'vccode',
            'delivery_cost',
            'delivery_num',
            'buyr_name',
        )

    def create(self, validated_data):
        """ 입력받은 주문 정보를 주문일자, 계산된 배송비와 함께 저장합니다. """
        order = Order.objects.create(**validated_data)

        # 주문일자 저장
        order.date = datetime.date.today()

        # 배송비 계산 후 저장
        if order.buyr_country.code == 'KR':
            order.delivery_cost = 3000
        else:
            rate = 1200  # 달러 환율
            delivery_cost = DeliveryCost.objects.get(country=order.buyr_country, quantity=order.quantity)
            order.delivery_cost = delivery_cost.cost / rate

        order.save()


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'pay_state',
        )
