# Generated by Django 4.1 on 2022-09-13 11:46

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='주문일자'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_cost',
            field=models.DecimalField(decimal_places=2, default=3000, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='배송비'),
        ),
        migrations.AlterField(
            model_name='order',
            name='pay_state',
            field=models.CharField(choices=[('결제완료', '결제완료'), ('상품준비중', '상품준비중'), ('배송중', '배송중'), ('배송완료', '배송완료'), ('결제취소', '결제취소')], default='결제완료', max_length=10, verbose_name='주문상태'),
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=16, validators=[django.core.validators.MinValueValidator(0)], verbose_name='가격'),
        ),
    ]
