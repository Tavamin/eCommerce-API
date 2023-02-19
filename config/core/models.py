from django.db import models

from product.models import Product


# Create your models here.


def check_inventory(product_id, user_quantity):
    product = Product.objects.get(id=product_id)
    if product.inventory >= user_quantity:
        return True
    return False

