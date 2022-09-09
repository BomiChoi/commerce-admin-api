from datetime import datetime

import pandas
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.country.models import Country, DeliveryCost
from apps.order.models import Order


class Command(BaseCommand):
    help = '엑셀 파일을 읽어 주문 데이터를 저장합니다.'

    @transaction.atomic
    def handle(self, *args, **options):
        df = pandas.read_excel('data/wanted_data.xlsx')
        for i, row in df.iterrows():
            # 날짜 변환
            date = datetime.strptime(str(row['Date']), '%Y%m%d').date()

            # 배송비
            delivery_cost = 0
            # 한국일 경우 배송비 3000원
            if row['buyr_country'] == 'KR':
                delivery_cost = 3000
            else:
                # 국가 코드로 찾기
                country = Country.objects.get(code=row['buyr_country'])
                # 이탈리아일 경우 스위스로 계산
                if row['buyr_country'] == 'IT':
                    country = Country.objects.get(code='CH')
                delivery_obj = DeliveryCost.objects.get(quantity=row['quantity'], country=country)
                delivery_cost = delivery_obj.cost

            Order.objects.create(
                date=date,
                pay_state=row['pay_state'],
                quantity=row['quantity'],
                price=row['price'],
                delivery_cost=delivery_cost,
                buyr_country=country,
                buyr_city=row['buyr_city'],
                buyr_zipcode=row['buyr_zipx'],
            )
