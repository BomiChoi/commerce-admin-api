from datetime import date

from django.core.validators import MinValueValidator
from django.db import models

from apps.common.models import TimeStampedModel


class CouponCategoryChoices(models.TextChoices):
    DELIVERY_COST = '배송비 할인', '배송비 할인'
    PERCENT = '% 할인', '% 할인'
    FIXED_AMOUNT = '정액 할인', '정액 할인'


class CouponType(models.Model):
    category = models.CharField(max_length=16, choices=CouponCategoryChoices.choices, verbose_name='유형')
    name = models.CharField(max_length=50, verbose_name='이름')
    value = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='할인값')
    issue_date = models.DateField(default=date.today, verbose_name='발급일')
    expr_date = models.DateField(null=True, blank=True, verbose_name='만료일')
    used_time = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='사용횟수')
    total_discount = models.DecimalField(max_digits=16, decimal_places=2, default=0, validators=[MinValueValidator(0)],
                                         verbose_name='총 할인액')

    class Meta:
        verbose_name = '쿠폰종류'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Coupon(TimeStampedModel):
    type = models.ForeignKey(CouponType, on_delete=models.CASCADE, verbose_name='종류')
    code = models.CharField(max_length=20, verbose_name='코드')
    is_used = models.BooleanField(default=False, verbose_name='사용여부')

    class Meta:
        verbose_name = '쿠폰'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.type}-{self.code}'
