from django.db import models
from product.models import Product, Discount


# Create your models here.


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    cost = models.FloatField()
    ORDER_STATUS_CHOICES = [('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'),
                            ('delivered', 'Delivered')]

    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='pending')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='orders')
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.status}"

    class Meta:
        ordering = ['created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')  # one to one
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.product} - {self.quantity}"


class Cart(models.Model):
    price = models.FloatField()
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='carts', null=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='carts')


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')  # one to one
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.product} - {self.quantity}"

    class Meta:
        ordering = ['product']
