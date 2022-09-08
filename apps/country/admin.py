from django.contrib import admin
from .models import Country, DeliveryCost


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'code',
        'dcode',
    )


@admin.register(DeliveryCost)
class DeliveryCostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'country',
        'quantity',
        'cost',
    )

