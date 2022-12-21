from django.db import models


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Discount(models.Model):
    DISCOUNT_CHOICES = [('percent', 'Percent'), ('amount', 'Amount')]
    kind = models.CharField(max_length=50, choices=DISCOUNT_CHOICES, default='percent')
    value = models.FloatField()
    voucher = models.CharField(max_length=90, unique=True, null=True, blank=True)
    expiry_date = models.DateTimeField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='discounts', null=True, blank=True)

    def __str__(self):
        return f"{self.kind} - {self.value}"


class Product(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField()
    description = models.TextField()
    price = models.FloatField(max_length=18)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    discounts = models.OneToOneField(Discount, on_delete=models.CASCADE, related_name='product', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='comments', null=True, blank=True)

    def __str__(self):
        return f" {self.product} - {self.user}"

    class Meta:
        ordering = ['content']



