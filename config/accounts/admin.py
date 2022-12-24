from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    search_fields = ['phone']
    list_display = ["email", "username"]


admin.site.register(CustomUser, CustomUserAdmin)