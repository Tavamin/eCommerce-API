import uuid

from django.db import models
from django.core.validators import MinValueValidator

from product.models import Product, Discount
from accounts.models import CustomUser


# Create your models here.


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    cost = models.FloatField()
    ORDER_STATUS_CHOICES = [('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'),
                            ('delivered', 'Delivered')]

    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='pending')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.status}"

    class Meta:
        ordering = ['created_at']
        permissions = [('cancel_order', 'Can cancel order')]



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')  # one to one
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.product} - {self.quantity}"


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='carts', null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='carts', null=True, blank=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])



    def __str__(self):
        return f"{self.product} - {self.quantity}"

    class Meta:
        ordering = ['product']
        unique_together = [['cart', 'product']]
