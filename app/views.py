from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import os

from .models import Cart, Customer, OrderPlaced, Product, CATEGORY_CHOICES
from .forms import CustomerRegistrationForm, CustomerProfileForm

from .custom_logger import logger


class ProductSneekPeak(View):
    # for home page
    def get(self, request):

        # Fetch first 3 product objects according to their categories
        categories = {}
        for i in CATEGORY_CHOICES:
            cat_code = i[0]
            cat_name = ''.join(i[1].strip().lower().split())
            cat_product = Product.objects.filter(category=cat_code)[:5]
            categories[cat_name] = cat_product
        logger.critical(categories)
        return render(request, 'app/home.html', categories)


class ProductDetailView(View):
    # for product page
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        cart_state = False
        try:
            cart_state = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()
        except:
            pass
        return render(request, 'app/productdetail.html', {'product': product, 'cart_state': cart_state})


@login_required
def add_to_cart(request):
    # for add to cart in db
    user = request.user
    product_id = request.GET.get("product_id")
    if product_id is not None:
        cart = Cart.objects.filter(user=user, product=product_id)
        if cart:
            logger.error("product already exists! Skipping addition to cart")
            logger.error(cart)
        else:
            # add product only if its not present
            product = Product.objects.get(id=product_id)
            Cart(user=user, product=product).save()
    return redirect("/cart")


def calculateAmounts(cart):
    # Calculate total amounts based on cart objects
    if cart:
        amounts = []
        shipping = 50.0
        for i in cart:
            quantity = i.quantity
            price = i.product.discounted_price * quantity
            amounts.append(price)
        total_amt = sum(amounts)
        if total_amt >= 500:
            shipping = 0.0
        total_amt += shipping

        final_amounts = {
            'shippingamount': shipping,
            'finalamount': total_amt,
            'totalamount': sum(amounts),
        }
        return final_amounts
    else:
        return


@login_required
def view_cart(request):
    # for cart page
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        if cart:
            final_amounts = calculateAmounts(cart)
            return render(request, 'app/addtocart.html', {'carts': cart, 'amounts': final_amounts, 'cartempty': False})
        else:
            return render(request, 'app/addtocart.html', {'cartempty': True})


@login_required
def plus_cart_item(request):
    # for plus button in cart page
    if request.method == 'GET':
        product_id = request.GET['product_id']
        cart_product = Cart.objects.get(
            Q(product=product_id) & Q(user=request.user))
        cart_product.quantity += 1
        cart_product.save()

        cart = Cart.objects.filter(user=request.user)
        if cart:
            data = calculateAmounts(cart)
            data['quantity'] = cart_product.quantity
            return JsonResponse(data)
        else:
            return JsonResponse({'empty': True})


@login_required
def minus_cart_item(request):
    # for minus button in cart page
    if request.method == 'GET':
        product_id = request.GET['product_id']
        cart_product = Cart.objects.get(
            Q(product=product_id) & Q(user=request.user))
        cart_product.quantity -= 1
        if cart_product.quantity < 1:
            logger.error("cart quantity was below 1, setting to 1")
            cart_product.quantity = 1
        cart_product.save()

        cart = Cart.objects.filter(user=request.user)
        if cart:
            data = calculateAmounts(cart)
            data['quantity'] = cart_product.quantity
            return JsonResponse(data)
        else:
            return JsonResponse({'empty': True})


@login_required
def remove_cart_item(request):
    # for delete button in cart page
    if request.method == 'GET':
        product_id = request.GET['product_id']
        cart_product = Cart.objects.get(
            Q(product=product_id) & Q(user=request.user))
        cart_product.delete()

        cart = Cart.objects.filter(user=request.user)
        if cart:
            data = calculateAmounts(cart)
            data['quantity'] = cart_product.quantity
            return JsonResponse(data)
        else:
            return JsonResponse({'empty': True})


@login_required
def buy_now(request, pk):
    user = request.user
    product = Product.objects.get(id=pk)
    addresses = Customer.objects.filter(user=user)

    quantity = 1
    total_amt = quantity * product.discounted_price
    shipping = 50 if total_amt < 500 else 0
    final_amt = total_amt + shipping

    final_amounts = {
        'shippingamount': shipping,
        'finalamount': final_amt,
        'totalamount': total_amt,
    }

    # get the PayPal Client ID from OS environment variables
    client_id = os.environ.get('PAYPAL-CLIENTID')

    # Calculating USD from INR for Payment
    usd_amount = round(final_amt/76.88, 2)
    logger.critical('Converting INR ' + str(final_amt) +
                    ' to USD ' + str(usd_amount))

    return render(request, 'app/buynow.html', {'addresses': addresses, 'amounts': final_amounts, 'paypal_clientid': client_id, 'product': product, 'quantity': quantity, 'usd_amount': usd_amount})


@login_required
def orders(request):
    orders = OrderPlaced.objects.filter(
        user=request.user).order_by('-ordered_date')
    return render(request, 'app/orders.html', {'order_placed': orders})


def ram(request, data=None):
    # for ram page
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

def solidstatedrive(request, data=None):
    # for ssd page
    if data == None:
        solidstatedrives = Product.objects.filter(category='SSD')
    elif str(data).lower() == 'samsung' or str(data).lower() == 'wd':
        solidstatedrives = Product.objects.filter(category='SSD').filter(brand=data)

    elif str(data) == 'below4000':
        solidstatedrives = Product.objects.filter(
            category='SSD').filter(discounted_price__lt=4000)

    elif str(data) == 'above4000':
        solidstatedrives = Product.objects.filter(
            category='SSD').filter(discounted_price__gt=4000)

    return render(request, 'app/solidstatedrive.html', {'solidstatedrives': solidstatedrives})

@login_required
def checkout(request):
    user = request.user
    addresses = Customer.objects.filter(user=user)
    carts = Cart.objects.filter(user=user)
    final_amounts = calculateAmounts(carts)

    # get the PayPal Client ID from OS environment variables
    client_id = os.environ.get('PAYPAL-CLIENTID')

    # Calculating USD from INR for Payment
    inr_amount = final_amounts['finalamount']
    usd_amount = round(inr_amount/76.88, 2)
    logger.critical('Converting INR ' + str(inr_amount) +
                    ' to USD ' + str(usd_amount))

    return render(request, 'app/checkout.html', {'addresses': addresses, 'cartitems': carts, 'amounts': final_amounts, 'paypal_clientid': client_id, 'usd_amount': usd_amount})


@login_required
def buy_now_payment_done(request):
    # called when order is placed directly
    user = request.user
    custid = request.GET.get('custid')
    product_id = request.GET.get('prod_id')
    quantity = request.GET.get('prod_quant')
    
    customer = Customer.objects.get(id=custid)
    product = Product.objects.get(id=product_id)

    OrderPlaced(user=user, customer=customer, product=product, quantity=quantity).save()
    return redirect('orders')


# @login_required(login_url='/accounts/login/')
@login_required
def payment_done(request):
    # called when order is placed through cart
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)

    for c in cart:
        OrderPlaced(user=user, customer=customer,
                    product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')


class CustomerRegistrationView(View):
    # for register page
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Account created Successfully!')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class AddressView(View):
    # for address page
    def get(self, request):
        form = CustomerProfileForm()
        address = Customer.objects.filter(user=request.user)
        return render(request, 'app/address.html', {'form': form, 'address': address, 'active': 'btn-primary'})

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
            reg = Customer(user=user, name=name, phone=phone,
                           locality_address=locality_address, city=city, state=state, zipcode=zipcode)
            reg.save()

            # messages.success(request, 'Customer Profile has been Added!')
        return redirect('address')
        # return render(request, 'app/address.html', {'form': form, 'active': 'btn-primary'})


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    # for profile page
    def get(self, request):
        return render(request, 'app/profile.html', {'active': 'btn-primary'})
    # def get(self, request):
    #     form = CustomerProfileForm()
    #     return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    # def post(self, request):
    #     form = CustomerProfileForm(request.POST)
    #     if form.is_valid():
    #         user = request.user
    #         name = form.cleaned_data['name']
    #         phone = form.cleaned_data['phone']
    #         locality_address = form.cleaned_data['locality_address']
    #         city = form.cleaned_data['city']
    #         state = form.cleaned_data['state']
    #         zipcode = form.cleaned_data['zipcode']
    #         reg = Customer(user=user, name=name, phone=phone, locality_address=locality_address, city=city, state=state, zipcode=zipcode)
    #         reg.save()

    #         messages.success(request, 'Customer Profile has been Added!')
    #     return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})


@login_required
def delete_customer(request, id):
    # for deleting customer address
    ob = Customer.objects.get(id=id)
    ob.delete()
    return redirect('address')
