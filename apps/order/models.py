from datetime import date

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.country.models import Country
from apps.coupon.models import Coupon


class OrderStatusChoices(models.TextChoices):
    PAID = '결제완료', '결제완료'
    READY = '상품준비중', '상품준비중'
    SHIPPING = '배송중', '배송중'
    SHIPPED = '배송완료', '배송완료'
    CANCELLED = '결제취소', '결제취소'


class Order(models.Model):
    date = models.DateField(default=date.today, verbose_name='주문일자')
    pay_state = models.CharField(max_length=10, choices=OrderStatusChoices.choices, default='결제완료', verbose_name='주문상태')
    quantity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(72)], verbose_name='수량')
    price = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='금액')
    delivery_cost = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)], default=3000,
                                        verbose_name='배송비')
    buyr_country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='배송국가')
    buyr_city = models.CharField(max_length=50, null=True, blank=True, verbose_name='배송도시')
    buyr_zipcode = models.CharField(max_length=10, verbose_name='우편번호')
    buyr_name = models.CharField(max_length=30, verbose_name='주문자명')
    delivery_num = models.CharField(max_length=20, null=True, blank=True, verbose_name='송장번호')
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.PROTECT, verbose_name='쿠폰')

    class Meta:
        verbose_name = '주문내역'
        verbose_name_plural = verbose_name
