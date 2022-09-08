from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'pay_state',
        'quantity',
        'price',
        'delivery_cost',
        'buyr_country',
        'buyr_zipcode',
        'buyr_name',
        'delivery_num',
    )
