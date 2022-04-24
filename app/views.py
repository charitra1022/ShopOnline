from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages

from .models import Customer, Product, CATEGORY_CHOICES
from .forms import CustomerRegistrationForm, CustomerProfileForm


# from .models import Cart, Customer, OrderPlaced


class ProductSneekPeak(View):
    def get(self, request):

        # Fetch first 3 product objects according to their categories
        categories = {}
        for i in CATEGORY_CHOICES:
            cat_code = i[0]
            cat_name = ''.join(i[1].strip().lower().split())
            cat_product = Product.objects.filter(category=cat_code)[:5]
            categories[cat_name] = cat_product

        # topwears = Product.objects.filter(category='TW')
        # bottomwears = Product.objects.filter(category='BW')
        # rams = Product.objects.filter(category='RAM')
        # laptops = Product.objects.filter(category='L')

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
    address = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'address': address, 'active': 'btn-primary'})


def orders(request):
    return render(request, 'app/orders.html')


def ram(request, data=None):
    if data == None:
        rams = Product.objects.filter(category='RAM')
    elif str(data).lower() == 'corsair' or str(data).lower() == 'crucial':
        rams = Product.objects.filter(category='RAM').filter(brand=data)

    elif str(data) == 'below2000':
        rams = Product.objects.filter(
            category='RAM').filter(discounted_price__lt=2000)

    elif str(data) == 'above2000':
        rams = Product.objects.filter(
            category='RAM').filter(discounted_price__gt=2000)

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


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            locality_address = form.cleaned_data['locality_address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, phone=phone, locality_address=locality_address, city=city, state=state, zipcode=zipcode)
            reg.save()

            messages.success(request, 'Customer Profile has been Added!')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})


def delete_customer(request, id):
    ob = Customer.objects.get(id=id)
    ob.delete()
    return redirect('address')
