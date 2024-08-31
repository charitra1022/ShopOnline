from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError

import os
from itertools import chain
from datetime import datetime
from enum import Enum

from .models import Cart, Customer, Product, Order, OrderDetail, CATEGORY_CHOICES
from .forms import CustomerRegistrationForm, CustomerProfileForm, MyPasswordResetForm

from .custom_logger import logger
from .invoice import createInvoice

########################### Helper Functions #######################

class Payment_Modes(Enum):
    """Define the various payment options we have"""
    COD = "Cash on Delivery"
    PAYPAL = "PayPal"
    ONLINE = "Online"


def generate_transaction_id(length=12):
    import random
    import string
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

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


def generateOrderId(userId:int, orderCount:int):
    """
    Generates Order ID of format ODYYYYMMDDUUUUUOOOOO.
    
    Annotations:
        Consider order datetime -> 25 May, 2022, 18:45:56

        YYYY - complete year. Ex- 2022
        MM  - month. Ex- 05
        DD - date. Ex- 25
        UUUUU - 5 char long user id
        OOOOO - 5 char long order count of the user

    Parameters:
        userId (int): User id of orderer
        orderCount (int): Number of orders placed by current user at present
    """

    formatted_datetime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    dateStr, timeStr = formatted_datetime.split()
    date, month, year = dateStr.split('-')
    # hh, mm, ss = timeStr.split(':')

    order_count = str(orderCount).zfill(5)
    user_id = str(userId).zfill(5)
    # order_id = f"OD{year}{month}{date}{hh}{mm}{ss}{user_id}{order_count}"
    order_id = f"OD{year}{month}{date}{user_id}{order_count}"

    return order_id



def generateInvoiceId(userId:int, orderCount:int, invoiceCount:int):
    """
    Generates Invoice ID of format INUUUUUOOOOOXX.
    
    Annotations:
        UUUUU - 5 char long user id
        OOOOO - 5 char long order count of the user
        XX - 2 char long invoice count of the user

    Parameters:
        userId (int): User id of orderer
        orderCount (int): Number of orders placed by current user at present
        invoiceCount (int): Number of invoices to be generated at incoming order
    """

    order_count = str(orderCount).zfill(5)
    user_id = str(userId).zfill(5)
    invoice_count = str(invoiceCount).zfill(2)
    invoice_id = f"IN{user_id}{order_count}{invoice_count}"

    return invoice_id



################### Basic Page Renderers #########################
@login_required
def orders(request):
    # orders = OrderPlaced.objects.filter(
    #     user=request.user).order_by('-ordered_date')

    orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    orderDetails = []

    for order in orders:
        orderDetailSet = OrderDetail.objects.filter(order__id=order.id)
        orderDetails.append(orderDetailSet)

    return render(request, 'app/orders.html', {'order_details': orderDetails})


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
            cat_product = Product.objects.filter(category=cat_code, stock__gt=0)[:5]
            categories[cat_name] = cat_product
        data = dict(categories)
        return render(request, 'app/home.html', data)


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
    if data is not None:
        data = " ".join(data.split("_"))
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
    if data is not None:
        data = " ".join(data.split("_"))
    if data == None:
        solidstatedrives = Product.objects.filter(category='SSD')
    elif str(data).lower() == 'samsung' or str(data).lower() == 'western digital':
        solidstatedrives = Product.objects.filter(
            category='SSD').filter(brand=data)

    elif str(data) == 'below4000':
        solidstatedrives = Product.objects.filter(
            category='SSD').filter(discounted_price__lt=4000)

    elif str(data) == 'above4000':
        solidstatedrives = Product.objects.filter(
            category='SSD').filter(discounted_price__gt=4000)

    return render(request, 'app/categories/solidstatedrive.html', {'solidstatedrives': solidstatedrives})


def cabinet(request, data=None):
    # for cabinet page
    if data is not None:
        data = " ".join(data.split("_"))
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
    if data is not None:
        data = " ".join(data.split("_"))
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
    if data is not None:
        data = " ".join(data.split("_"))
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
    if data is not None:
        data = " ".join(data.split("_"))
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
    if data is not None:
        data = " ".join(data.split("_"))
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
    if data is not None:
        data = " ".join(data.split("_"))
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
    if data is not None:
        data = " ".join(data.split("_"))
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
    if data is not None:
        data = " ".join(data.split("_"))
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
def order_placed_page(request):
    return render(request, 'app/thankyou.html')


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
    # txn_id = request.GET.get('txn_id')      # get txn id from the PayPal txn
    # txn_id = generate_transaction_id()      # PayPal stopped working so use random string as txn id
    txn_id = "-"                              # set to NULL as using Cash On Delivery
    payment_mode = Payment_Modes.COD

    tax = 0
    amount = calculateAmounts(cart)

    orderCount = Order.objects.filter(user=user).count()+1

    # Create a Order object
    order = Order(user=user, customer=customer, txn_id=txn_id)
    order.order_id = generateOrderId(user.id, orderCount)
    order.save()

    counter = 0
    for c in cart:
        counter+=1

        invoice_id = generateInvoiceId(user.id, orderCount, counter)
        client_details = [customer.name, customer.user.email]
        txn_details =  (txn_id, datetime.now(), amount['totalamount'], tax, invoice_id)
        products = [
            (c.product.title, c.quantity, c.product.discounted_price),
        ]

        createInvoice(client_details=client_details, txn_details=txn_details, products=products, payment_mode=payment_mode)

        # order = OrderPlaced(user=user, customer=customer,
        #             product=c.product, quantity=c.quantity, txn_id=txn_id)
        # order.invoice.name = f"invoice/{txn_id}.pdf"
        # order.order_id = generateOrderId(user.id, c.product.id)
        # order.save()

        # Create an OrderDetail object and link it to Order object
        order_detail = OrderDetail(order=order, product=c.product, quantity=c.quantity)
        order_detail.invoice.name = f"invoice/{invoice_id}.pdf"
        order_detail.invoice_id = invoice_id
        order_detail.save()

        c.delete()

        stock = c.product.stock - c.quantity
        Product.objects.filter(id=c.product.id).update(stock=stock)
    return redirect('order_placed')


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
    quantity = int(request.GET.get('prod_quant'))
    # txn_id = request.GET.get('txn_id')    # PayPal txn id
    # txn_id = generate_transaction_id()      # PayPal stopped working to use random txn id
    txn_id = "-"                              # set to NULL as using Cash On Delivery
    payment_mode = Payment_Modes.COD

    customer = Customer.objects.get(id=custid)
    product = Product.objects.get(id=product_id)

    amount = quantity * product.discounted_price
    tax = 0

    orderCount = Order.objects.filter(user=user).count()+1
    invoice_id = generateInvoiceId(user.id, orderCount, 1)

    client_details = [customer.name, customer.user.email]
    txn_details =  (txn_id, datetime.now(), amount, tax, invoice_id)
    products = [
        (product.title, quantity, product.discounted_price),
    ]

    createInvoice(client_details=client_details, txn_details=txn_details, products=products, payment_mode=payment_mode)


    # order = OrderPlaced(user=user, customer=customer, product=product, quantity=quantity, txn_id=txn_id)
    # order.invoice.name = f"invoice/{txn_id}.pdf"
    # order.order_id = generateOrderId(user.id, orderCount)
    # order.save()

    # Create a Order object
    order = Order(user=user, customer=customer, txn_id=txn_id)
    order.order_id = generateOrderId(user.id, orderCount)
    order.save()

    # Create an OrderDetail object and link it to Order object
    order_detail = OrderDetail(order=order, product=product, quantity=quantity)
    order_detail.invoice.name = f"invoice/{invoice_id}.pdf"
    order_detail.invoice_id = invoice_id
    order_detail.save()

    stock = product.stock - quantity
    Product.objects.filter(id=product.id).update(stock=stock)

    return redirect('order_placed')


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


def password_reset_request(request):
    # Called when password request is generated
    if request.method.lower() == "post":
        form = MyPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user_set = User.objects.filter(Q(email=email))

            if user_set.exists():
                user = user_set[0]
                subject = "Password Reset Request"
                template = "app/password/password_reset_email.txt"
                details = {
                    "user_first_name": user.first_name,
                    "user_email": user.email,
					"user": user,
					"protocol": "http",
					"domain": "127.0.0.1:8000",
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"token": default_token_generator.make_token(user),
					"site_name": "ShopOnline"
                }
                email_txt = render_to_string(template, details)
                try:
                    send_mail(subject, email_txt, os.environ.get('ADMIN_EMAIL'), [user.email], fail_silently=False)

                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                
                return redirect("password_reset_done")
            else:
                return redirect("password_reset_error")

    logger.critical("outside if statement")
    reset_form = MyPasswordResetForm()
    return render(request, "app/reset_password.html", {'form': reset_form})

def password_reset_error(request):
    return render(request, "app/reset_password_error.html")


def search(request):
    queryStr = request.GET.get('search', '')

    product_by_titles = Product.objects.filter(title__icontains=queryStr)
    product_by_brand = Product.objects.filter(brand__icontains=queryStr)
    
    products = list(set(list(chain(product_by_titles, product_by_brand))))
    return render(request, "app/search.html", {"products": products, "query": queryStr})



@login_required
def cancel_order(request, id):
    """
    :param id: id of the order to be cancelled

    for cancelling an order
    """
    order = Order.objects.get(id=id)
    order.status = "Cancel"
    order.save()
    return redirect("orders")
