import pandas
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.country.models import Country


class Command(BaseCommand):
    help = '엑셀 파일을 읽어 국가 데이터를 저장합니다.'

    @transaction.atomic
    def handle(self, *args, **options):
        df = pandas.read_excel('data/Country_code.xlsx')

        for i, row in df.iterrows():
            # Nambia 국가코드가 nan으로 인식되는 문제 해결
            if pandas.isna(row['country_code']):
                row['country_code'] = 'NA'
            
            Country.objects.create(
                name=row['country_name'],
                code=row['country_code'],
                dcode=row['country_dcode']
            )
