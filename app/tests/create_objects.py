from ..models import Product, Customer, OrderPlaced, Cart
from django.contrib.auth.models import User

import random
import string


#  create and return product object
def createProduct():
    title = "Test Product"
    selling_price = 20000.0
    discounted_price = 15500.56
    description = """This is a test product. theres nothing to see here"""
    brand = "TestBrand"
    category = "TST"
    product_image = "tests/productimg/boat-aux-cable-black.webp"

    return Product.objects.create(
        title=title,
        selling_price=selling_price,
        discounted_price=discounted_price,
        description=description,
        brand=brand,
        category=category,
        product_image=product_image
    )


# create and return customer object
def createCustomer():
    user = createUser()
    name = "Test Customer"
    phone = 1234567890
    locality_address = "add 1, add 2"
    city = "city"
    state = "state"
    zipcode = 123456

    return Customer.objects.create(
        user=user,
        name=name,
        phone=phone,
        locality_address=locality_address,
        city=city,
        state=state,
        zipcode=zipcode
    )


# create and return user object
def createUser():
    username = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))
    return User.objects.create_user(
        username=username,
        email='jlennon@beatles.com',
        password='glass onion'
    )


# create and return cart object
def createCart():
    user = createUser()
    product = createProduct()
    quantity = 10

    return Cart.objects.create(
        user=user,
        product=product,
        quantity=quantity
    )


# create and return orderplaced object
def createOrder():
    user = createUser()
    customer = createCustomer()
    product = createProduct()
    quantity = 10
    txn_id = "DEMOTRANSACTIONID"

    return OrderPlaced.objects.create(
        user=user,
        customer=customer,
        product=product,
        quantity=quantity,
        txn_id=txn_id
    )
