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

########################### Helper Functions #######################
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


################### Basic Page Renderers #########################
@login_required
def orders(request):
    orders = OrderPlaced.objects.filter(
        user=request.user).order_by('-ordered_date')
    return render(request, 'app/orders.html', {'order_placed': orders})


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


###################### Category page renderers ############################
def ram(request, data=None):
    # for ram page
    if data is not None: data = " ".join(data.split("_"))
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

    return render(request, 'app/categories/ram.html', {'rams': rams})

def solidstatedrive(request, data=None):
    # for ssd page
    if data is not None: data = " ".join(data.split("_"))
    if data == None:
        solidstatedrives = Product.objects.filter(category='SSD')
    elif str(data).lower() == 'samsung' or str(data).lower() == 'western digital':
        solidstatedrives = Product.objects.filter(category='SSD').filter(brand=data)

    elif str(data) == 'below4000':
        solidstatedrives = Product.objects.filter(
            category='SSD').filter(discounted_price__lt=4000)

    elif str(data) == 'above4000':
        solidstatedrives = Product.objects.filter(
            category='SSD').filter(discounted_price__gt=4000)

    return render(request, 'app/categories/solidstatedrive.html', {'solidstatedrives': solidstatedrives})

def cabinet(request, data=None):
    # for cabinet page
    if data is not None: data = " ".join(data.split("_"))
    if data == None:
        cabinets = Product.objects.filter(category='CB')
    elif str(data).lower() == 'samsung' or str(data).lower() == 'wd':
        cabinets = Product.objects.filter(category='CB').filter(brand=data)

    elif str(data) == 'below4000':
        cabinets = Product.objects.filter(
            category='CB').filter(discounted_price__lt=4000)

    elif str(data) == 'above4000':
        cabinets = Product.objects.filter(
            category='CB').filter(discounted_price__gt=4000)

    return render(request, 'app/categories/cabinet.html', {'cabinets': cabinets})


def pendrive(request, data=None):
    # for pendrive page
    if data is not None: data = " ".join(data.split("_"))
    if data == None:
        pendrives = Product.objects.filter(category='PND')
    elif str(data).lower() == 'samsung' or str(data).lower() == 'wd':
        pendrives = Product.objects.filter(category='PND').filter(brand=data)

    elif str(data) == 'below4000':
        pendrives = Product.objects.filter(
            category='PND').filter(discounted_price__lt=4000)

    elif str(data) == 'above4000':
        pendrives = Product.objects.filter(
            category='PND').filter(discounted_price__gt=4000)

    return render(request, 'app/categories/pendrive.html', {'pendrives': pendrives})

def ups(request, data=None):
    # for ups page
    if data is not None: data = " ".join(data.split("_"))
    if data == None:
        upss = Product.objects.filter(category='UPS')
    elif str(data).lower() == 'samsung' or str(data).lower() == 'wd':
        upss = Product.objects.filter(category='UPS').filter(brand=data)

    elif str(data) == 'below4000':
        upss = Product.objects.filter(
            category='UPS').filter(discounted_price__lt=4000)

    elif str(data) == 'above4000':
        upss = Product.objects.filter(
            category='UPS').filter(discounted_price__gt=4000)

    return render(request, 'app/categories/ups.html', {'upss': upss})

def keyboard(request, data=None):
    # for keyboard page
    if data is not None: data = " ".join(data.split("_"))
    if data == None:
        keyboards = Product.objects.filter(category='KB')
    elif str(data).lower() == 'samsung' or str(data).lower() == 'wd':
        keyboards = Product.objects.filter(category='KB').filter(brand=data)

    elif str(data) == 'below4000':
        keyboards = Product.objects.filter(
            category='KB').filter(discounted_price__lt=4000)

    elif str(data) == 'above4000':
        keyboards = Product.objects.filter(
            category='KB').filter(discounted_price__gt=4000)

    return render(request, 'app/categories/keyboard.html', {'keyboards': keyboards})

def hdd(request, data=None):
    # for hdd page
    if data is not None: data = " ".join(data.split("_"))
    if data == None:
        hdds = Product.objects.filter(category='HDD')
    elif str(data).lower() == 'samsung' or str(data).lower() == 'western digital':
        hdds = Product.objects.filter(category='HDD').filter(brand=data)

    elif str(data) == 'below4000':
        hdds = Product.objects.filter(
            category='HDD').filter(discounted_price__lt=4000)

    elif str(data) == 'above4000':
        hdds = Product.objects.filter(
            category='HDD').filter(discounted_price__gt=4000)

    return render(request, 'app/categories/hdd.html', {'harddiskdrives': hdds})

def psu(request, data=None):
    # for psu page
    if data is not None: data = " ".join(data.split("_"))
    if data == None:
        psus = Product.objects.filter(category='PSU')
    elif str(data).lower() == 'samsung' or str(data).lower() == 'wd':
        psus = Product.objects.filter(category='PSU').filter(brand=data)

    elif str(data) == 'below4000':
        psus = Product.objects.filter(
            category='PSU').filter(discounted_price__lt=4000)

    elif str(data) == 'above4000':
        psus = Product.objects.filter(
            category='PSU').filter(discounted_price__gt=4000)

    return render(request, 'app/categories/psu.html', {'psus': psus})

def motherboard(request, data=None):
    # for motherboard page
    if data is not None: data = " ".join(data.split("_"))
    if data == None:
        motherboards = Product.objects.filter(category='MB')
    elif str(data).lower() == 'samsung' or str(data).lower() == 'wd':
        motherboards = Product.objects.filter(category='MB').filter(brand=data)

    elif str(data) == 'below4000':
        motherboards = Product.objects.filter(
            category='MB').filter(discounted_price__lt=4000)

    elif str(data) == 'above4000':
        motherboards = Product.objects.filter(
            category='MB').filter(discounted_price__gt=4000)

    return render(request, 'app/categories/motherboard.html', {'motherboards': motherboards})

def mouse(request, data=None):
    # for mouse page
    if data is not None: data = " ".join(data.split("_"))
    if data == None:
        mouses = Product.objects.filter(category='MOU')
    elif str(data).lower() == 'samsung' or str(data).lower() == 'wd':
        mouses = Product.objects.filter(category='MOU').filter(brand=data)

    elif str(data) == 'below4000':
        mouses = Product.objects.filter(
            category='MOU').filter(discounted_price__lt=4000)

    elif str(data) == 'above4000':
        mouses = Product.objects.filter(
            category='MOU').filter(discounted_price__gt=4000)

    return render(request, 'app/categories/mouse.html', {'mouses': mouses})


####################### Cart Related ######################
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


############################ Buy Now Related #########################
@login_required
def buy_now(request, pk):
    # Called when buy now button is clicked
    product = Product.objects.get(id=pk)
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

    return render(request, 'app/buynow.html', {'amounts': final_amounts, 'paypal_clientid': client_id, 'product': product, 'quantity': quantity, 'usd_amount': usd_amount})


@login_required
def buynowcheckout(request):
    # Called when order is placed from buy now page
    user = request.user
    product_id = request.POST.get('prod_id')
    quantity = int(request.POST.get('prod_quant'))

    product = Product.objects.get(id=product_id)
    addresses = Customer.objects.filter(user=user)

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

    return render(request, 'app/buynowcheckout.html', {'addresses': addresses, 'paypal_clientid': client_id, 'amounts': final_amounts, 'product': product, 'quantity': quantity, 'usd_amount': usd_amount})


@login_required
def buy_now_payment_done(request):
    # called when payment has been done after buy now functionality
    user = request.user
    custid = request.GET.get('custid')
    product_id = request.GET.get('prod_id')
    quantity = request.GET.get('prod_quant')
    
    customer = Customer.objects.get(id=custid)
    product = Product.objects.get(id=product_id)

    OrderPlaced(user=user, customer=customer, product=product, quantity=quantity).save()

    return redirect('orders')




########################### Address and Customer Related ############################
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


@login_required
def delete_customer(request, id):
    # for deleting customer address
    ob = Customer.objects.get(id=id)
    ob.delete()
    return redirect('address')
