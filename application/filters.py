from .models import *
import django_filters


class OnlineShopFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'category': ['exact'],
            'price': ['lte', 'gte'],
        }
