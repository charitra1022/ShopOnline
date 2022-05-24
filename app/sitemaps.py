from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Product

class StaticViewSitemap(Sitemap):
  # Give sitemap urls for static urls
  def items(self):
    views = ['ram', 'solidstatedrive', 'cabinet', 'pendrive', 'ups', 'keyboard', 'psu', 'motherboard', 'mouse',]
    # hdd not added

    return views

  def location(self, item):
    return reverse(item)


class ProductSitemap(Sitemap):
  # Give sitemap urls for products
  def items(self):
    return Product.objects.all()
