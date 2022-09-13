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
        countries = pandas.read_excel('data/DeliveryCost.xlsx').columns[2:]
        
        for i, row in df.iterrows():
            # 날짜 변환
            date = datetime.strptime(str(row['Date']), '%Y%m%d').date()
            # 국가 코드로 찾기
            country = Country.objects.get(code=row['buyr_country'])
            # 주문 생성
            order = Order.objects.create(
                date=date,
                pay_state=row['pay_state'],
                quantity=row['quantity'],
                price=row['price'],
                buyr_country=country,
                buyr_city=row['buyr_city'],
                buyr_zipcode=row['buyr_zipx'],
            )

            # 해외 배송비 책정
            if row['buyr_country'] != 'KR':
                # 배송비 데이터 없는 국가일 경우 미국 기준으로 책정
                if country.name not in countries:
                    country = Country.objects.get(code='US')
                delivery_obj = DeliveryCost.objects.get(quantity=row['quantity'], country=country)
                delivery_cost = delivery_obj.cost
                # 환율 적용 후 배송비 저장
                rate = 1200
                order.delivery_cost = delivery_cost / rate
                order.save()
