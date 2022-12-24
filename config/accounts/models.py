from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    username = models.CharField(max_length=14, validators=[
        RegexValidator(
            regex='^(0|\+98)?[1-9]+[\d]{9}$',
            message='Phone number must be valid',
            code='invalid_phone'
        )
    ], unique=True)
    USERNAME_FIELD = 'username'


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
