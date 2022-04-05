import re
from unicodedata import category
from django.shortcuts import render
from django.views import View
from django.contrib import messages

from .models import Product
from .forms import CustomerRegistrationForm


# from .models import Cart, Customer, OrderPlaced


class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        rams = Product.objects.filter(category='RAM')
        laptops = Product.objects.filter(category='L')
        categories = {
            "topwears": topwears,
            "bottomwears": bottomwears,
            "rams": rams,
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


def ram(request, data=None):
    if data==None:
        rams = Product.objects.filter(category='RAM')
    elif str(data).lower()=='samsung' or str(data).lower()=='redmi':
        rams = Product.objects.filter(category='RAM').filter(brand=data)

    elif str(data)=='below10000':
        rams = Product.objects.filter(category='RAM').filter(discounted_price__lt=10000)
    
    elif str(data)=='above10000':
        rams = Product.objects.filter(category='RAM').filter(discounted_price__gt=10000)

    return render(request, 'app/ram.html', {'rams': rams})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Account created Successfully!')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})


def checkout(request):
    return render(request, 'app/checkout.html')
