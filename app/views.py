from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.db.models import Q

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
        return render(request, 'app/home.html', categories)


class ProductDetailView(View):
    # for product page
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', {'product': product})


def add_to_cart(request):
    # for add to cart in db
    user = request.user
    product_id = request.GET.get("product_id")
    if product_id is not None:
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


def view_cart(request):
    # for cart page
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        if cart:
            final_amounts = calculateAmounts(cart)
            return render(request, 'app/addtocart.html', {'carts': cart, 'amounts': final_amounts, 'cartempty': False})
        else:
            return render(request, 'app/addtocart.html', {'cartempty': True})


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


def minus_cart_item(request):
    # for minus button in cart page
    if request.method == 'GET':
        product_id = request.GET['product_id']
        cart_product = Cart.objects.get(
            Q(product=product_id) & Q(user=request.user))
        cart_product.quantity -= 1
        if cart_product.quantity<1:
            logger.error("cart quantity was below 1, setting to 1")
            cart_product.quantity=1
        cart_product.save()

        cart = Cart.objects.filter(user=request.user)
        if cart:
            data = calculateAmounts(cart)
            data['quantity'] = cart_product.quantity
            return JsonResponse(data)
        else:
            return JsonResponse({'empty': True})


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


def buy_now(request):
    return render(request, 'app/buynow.html')


def orders(request):
    return render(request, 'app/orders.html')


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


def checkout(request):
    user = request.user
    addresses = Customer.objects.filter(user=user)
    carts = Cart.objects.filter(user=user)

    final_amounts = calculateAmounts(carts)

    return render(request, 'app/checkout.html', {'addresses': addresses, 'cartitems': carts, 'amounts': final_amounts})


def payment_done(request):
    # called when order is placed
    user = request.user
    custid = request.GET.get('custid')
    logger.error(custid)

    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)

    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
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


def delete_customer(request, id):
    # for deleting customer address
    ob = Customer.objects.get(id=id)
    ob.delete()
    return redirect('address')
