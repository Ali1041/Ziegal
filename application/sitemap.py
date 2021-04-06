from django.contrib import sitemaps
from .models import Product,Blog
from django.urls import reverse, reverse_lazy


class StaticPages(sitemaps.Sitemap):

    def items(self):
        return [
            'home',
            'dual-sims',
            'monthly-deals',
            'wishlist',
            'online-shop',
            'z-wifi',
            'broadband_deals',
            'privacy-policy',
            'mission-statement',
            'terms-condition',
            'blog-list',
        ]

    def location(self, obj):
        return reverse(obj)


class ProductsMap(sitemaps.Sitemap):

    def items(self):
        return Product.objects.all()


class BlogsMap(sitemaps.Sitemap):

    def items(self):
        return Blog.objects.all()
