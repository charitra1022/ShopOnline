from django.test import TestCase
from ..models import Product
from .create_objects import *

# Product database test
class ProductTestCase(TestCase):
    def test_product_creation(self):
        t = createProduct()
        self.assertTrue(isinstance(t, Product))
        self.assertEqual(t.__str__(), str(t.id))

