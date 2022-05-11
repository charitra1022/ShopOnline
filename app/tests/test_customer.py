from django.test import TestCase
from ..models import Customer
from django.contrib.auth.models import User

class CustomerTestCase(TestCase):
    def create_customer_object(self,
        user,
        name="Test Customer",
        phone=1234567890,
        locality_address="add 1, add 2",
        city="city",
        state="state",
        zipcode=123456
    ):
        return Customer.objects.create(
            user=user,
            name=name,
            phone=phone,
            locality_address=locality_address,
            city=city,
            state=state,
            zipcode=zipcode
        )

    def test_customer_creation(self):
        user = User.objects.create_user(
            username='john',
            email='jlennon@beatles.com',
            password='glass onion'
        )
        t = self.create_customer_object(user=user)
        self.assertTrue(isinstance(t, Customer))
        self.assertEqual(t.__str__(), str(t.id))
