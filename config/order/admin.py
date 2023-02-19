from django.contrib import admin, messages
from django.db.models import Count, QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse

from .models import Order, OrderItem, Cart, CartItem


# Register your models here.

class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num = 1
    # max_num = 20
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    inlines = [OrderItemInline]
    list_display = ['id', 'created_at', 'user', 'status']
    list_editable = ['status']
    list_per_page = 10




class CartItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num = 1
    # max_num = 20
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ['id', 'discount', 'user']
    list_per_page = 10
