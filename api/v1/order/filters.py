import django_filters
from django_filters import rest_framework as filters

from apps.order.models import Order


class OrderFilter(filters.FilterSet):
    date_gte = django_filters.DateTimeFilter(field_name="date", lookup_expr='gte')
    date_lte = django_filters.DateTimeFilter(field_name="date", lookup_expr='lte')

    class Meta:
        model = Order
        fields = ['pay_state', 'date_gte', 'date_lte']
