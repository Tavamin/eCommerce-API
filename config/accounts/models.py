from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    username = models.CharField(max_length=14, validators=[
        RegexValidator(
            regex='^(0|\+98)?[1-9][\d]{9}$',
            message='Phone number must be valid',
            code='invalid_phone'
        )
    ], unique=True)
    USERNAME_FIELD = 'username'


    def __str__(self):
        return f"{self.username}"


class Address(models.Model):
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.address}"

    class Meta:
        ordering = ['is_default']


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer')
    birth_date = models.DateField(null=True, blank=True)
    addresses = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='customers', null=True, blank=True)

    def __str__(self):
        return f"{self.user}"

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name


    class Meta:
        ordering = ['user__first_name', 'user__last_name']
