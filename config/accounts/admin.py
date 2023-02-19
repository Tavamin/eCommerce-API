from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Customer


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    search_fields = ['phone']
    list_display = ["email", "username"]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ["first_name", "last_name"]
    list_per_page = 10
    list_select_related = ["user"]
    search_fields = ["user__first_name", "user__last_name", "user__phone"]


admin.site.register(Customer, CustomerAdmin)
