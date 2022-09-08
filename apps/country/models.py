from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Country(models.Model):
    name = models.CharField(max_length=50, verbose_name='국가명')
    code = models.CharField(max_length=2, verbose_name='국가코드')
    dcode = models.CharField(max_length=4, verbose_name='국가번호')

    class Meta:
        verbose_name = '국가'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class DeliveryCost(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='국가')
    quantity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(72)], verbose_name='수량')
    cost = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='비용')

    class Meta:
        verbose_name = '배송비'
        verbose_name_plural = verbose_name
