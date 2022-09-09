import pandas
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.country.models import Country, DeliveryCost


class Command(BaseCommand):
    help = '엑셀 파일을 읽어 배송비 데이터를 저장합니다.'

    @transaction.atomic
    def handle(self, *args, **options):
        df = pandas.read_excel('data/DeliveryCost.xlsx')

        for i, row in df.iterrows():
            quantity = row['quantity']
            
            for col in df.columns[2:]:
                DeliveryCost.objects.create(
                    country=Country.objects.get(name=col),
                    quantity=quantity,
                    cost=row[col]
                )
