from django.test import TestCase

from app.tests.create_objects import createCart, createCustomer
from ..models import Cart

class CartTestCase(TestCase):
    def test_cart_creation(self):
        t = createCart()
        price = t.quantity * t.product.discounted_price

        self.assertTrue(isinstance(t, Cart))
        self.assertEqual(t.__str__(), str(t.id))
        self.assertEqual(t.total_price, price)