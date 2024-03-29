from django.db import models

from accounts.models import Customer


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
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='discounts', null=True, blank=True)

    def __str__(self):
        return f"{self.kind} - {self.value}"


class Product(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(null=True, blank=True)
    price = models.FloatField(max_length=18)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    discounts = models.OneToOneField(Discount, on_delete=models.CASCADE, related_name='product', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class HaveDiscount(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='have_discounts')
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='have_discounts')

    def __str__(self):
        return f"{self.user} - {self.discount}"

    class Meta:
        unique_together = ('user', 'discount')


class Comment(models.Model):

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    # if user is not logged in then we will use email
    email = models.EmailField(null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)




    def __str__(self):
        return f" {self.product} - {self.user}"

    class Meta:
        ordering = ['content']
