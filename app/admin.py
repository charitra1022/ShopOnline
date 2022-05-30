from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode

from .models import (
    Customer, Product, Cart, Order, OrderDetail
)


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'phone', 'locality_address', 'city', 
                    'state', 'zipcode']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'stock', 'selling_price', 'discounted_price',
                    'description', 'brand', 'category', 'product_image']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'product_info', 'quantity']

    def product_info(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)


# @admin.register(OrderPlaced)
# class OrderPlacedModelAdmin(admin.ModelAdmin):
#     list_display = ['id', 'order_id', 'user', 'customer', 'customer_info', 'product', 'product_info', 'quantity',
#                     'ordered_date', 'status', 'txn_id']
    
#     def customer_info(self, obj):
#         link = reverse("admin:app_customer_change", args=[obj.customer.pk])
#         return format_html('<a href="{}">{}</a>', link, obj.customer.name)

#     def product_info(self, obj):
#         link = reverse("admin:app_product_change", args=[obj.product.pk])
#         return format_html('<a href="{}">{}</a>', link, obj.product.title)


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id_', 'user', 'customer', 'customer_info',
                    'ordered_date', 'status', 'txn_id']
    
    def customer_info(self, obj):
        link = reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)

    def product_info(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)
    
    def order_id_(self, obj):
        link = reverse("admin:app_orderdetail_changelist") + "?" + urlencode({"order__id": f"{obj.id}"})
        return format_html('<a href="{}">{}</a>', link, obj.order_id)



@admin.register(OrderDetail)
class OrderDetailModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_info', 'product', 'product_info', 'quantity', 'invoice_']
    
    def order_info(self, obj):
        link = reverse("admin:app_order_change", args=[obj.order.pk])
        return format_html('<a href="{}">{}</a>', link, obj.order.order_id)

    def product_info(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

    def invoice_(self, obj):
        link = obj.invoice.url
        return format_html('<a href="{}" target="_blank">{}</a>', link, obj.invoice_id)
