from unicodedata import category
from django.shortcuts import render
from django.views import View

from .models import Product


# from .models import Cart, Customer, OrderPlaced


class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        categories = {
            "topwears": topwears,
            "bottomwears": bottomwears,
            "mobiles": mobiles,
            "laptops": laptops,
        }
        return render(request, 'app/home.html', categories)


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', {'product': product})


def add_to_cart(request):
    return render(request, 'app/addtocart.html')


def buy_now(request):
    return render(request, 'app/buynow.html')


def profile(request):
    return render(request, 'app/profile.html')


def address(request):
    return render(request, 'app/address.html')


def orders(request):
    return render(request, 'app/orders.html')


def change_password(request):
    return render(request, 'app/changepassword.html')


def mobile(request, data=None):
    if data==None:
        mobiles = Product.objects.filter(category='M')
    elif str(data).lower()=='samsung' or str(data).lower()=='redmi':
        mobiles = Product.objects.filter(category='M').filter(brand=data)

    elif str(data)=='below10000':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    
    elif str(data)=='above10000':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)

    return render(request, 'app/mobile.html', {'mobiles': mobiles})


def login(request):
    return render(request, 'app/login.html')


def customerregistration(request):
    return render(request, 'app/customerregistration.html')


def checkout(request):
    return render(request, 'app/checkout.html')
