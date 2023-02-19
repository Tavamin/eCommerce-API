from django.contrib import admin, messages
from django.db.models import Count, QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse

from .models import Product, Category, HaveDiscount, Discount


# Register your models here.

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('>10', 'OK')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        elif self.value() == '>10':
            return queryset.filter(inventory__gte=10)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title']
    autocomplete_fields = ['category']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    list_display = ['title', 'price', 'inventory_status', 'category_title']  # add tables
    list_editable = ['price']  # make field editable
    list_filter = ['category', 'last_update', InventoryFilter]
    list_per_page = 10  # numbers of items that show in each page
    list_select_related = ['category']  # for less query in database

    @admin.display(ordering='inventory')  # for add ordering for this computed column
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return "OK"

    @admin.display(ordering='collection')
    def category_title(self, product):
        return product.category.title

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset: QuerySet):
        updated_count = queryset.update(inventory=0)
        self.message_user(request,
                          f"{updated_count} product were successfully updated",
                          messages.SUCCESS
                          )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'products_count']  # add tables
    # list_editable = ['title']  # make field editable
    list_per_page = 10  # numbers of items that show in each page

    @admin.display(ordering='products_count')
    def products_count(self, category):
        url = (reverse('admin:product_product_changelist')  # app_model_page
               + "?"
               + urlencode({'category__id': str(category.id)})
               )
        return format_html('<a href="{}">{}</a>', url, category.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )



@admin.register(HaveDiscount)
class HaveDiscountAdmin(admin.ModelAdmin):
    list_per_page = 10


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_per_page = 10

