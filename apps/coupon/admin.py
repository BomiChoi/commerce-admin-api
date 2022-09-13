from django.contrib import admin

from .models import Coupon, CouponType


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'type',
        'code',
        'is_used',
        'created_at',
        'updated_at',
    )


class CouponInline(admin.TabularInline):
    model = Coupon


@admin.register(CouponType)
class CouponTypeAdmin(admin.ModelAdmin):
    inlines = (CouponInline,)
    list_display = (
        'id',
        'category',
        'name',
        'value',
        'issue_date',
        'expr_date',
        'used_time',
        'total_discount',
    )
