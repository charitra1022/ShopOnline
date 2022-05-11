from django.test import TestCase

from app.tests.create_objects import createCustomer
from ..models import Customer

class CustomerTestCase(TestCase):
    def test_customer_creation(self):
        t = createCustomer()
        self.assertTrue(isinstance(t, Customer))
        self.assertEqual(t.__str__(), str(t.id))
