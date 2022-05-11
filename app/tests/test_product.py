from django.test import TestCase
from ..models import Product

# Product database test
class ProductTestCase(TestCase):
    def create_product_object(self, 
            title="Test Product", 
            selling_price = 20000.0,
            discounted_price = 15500.56,
            description = """This is a test product. theres nothing to see here""",
            brand = "TestBrand",
            category = "TST",
            product_image = "tests/productimg/boat-aux-cable-black.webp"
    ):
        return Product.objects.create(
            title=title,
            selling_price=selling_price,
            discounted_price=discounted_price,
            description=description,
            brand=brand,
            category=category,
            product_image=product_image
        )

    def test_product_creation(self):
        t = self.create_product_object()
        self.assertTrue(isinstance(t, Product))
        self.assertEqual(t.__str__(), str(t.id))

