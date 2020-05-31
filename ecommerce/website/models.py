from django.db import models
from django.conf import settings
from django_mysql.models import ListCharField
from django.shortcuts import reverse
from django_countries.fields import CountryField

STATUS_CHOICES = (
    ('N','new'),
    ('P','popular'),
    ('S','sale')
)
CATEGORY_CHOICES = (
    ('MW','Mens Wear'),
    ('WW', 'Womens Wear'),
    ('EC', 'Electronics'),
    ('FW', 'Foot Wear')
)

class Item(models.Model):
    title = models.CharField(max_length=64)
    price = models.FloatField()
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1)
    tags = ListCharField(
          base_field= models.CharField(max_length=15),
          size = 10,
          max_length =(10 * 16)
    )
    slug = models.SlugField()
    description = models.TextField()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart",kwargs={
            'slug': self.slug
        })

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete= models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.item.title} x {self.quantity}"

    def get_total_price(self):
        return self.quantity * self.item.price


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress',on_delete=models.SET_NULL,blank=True,null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_price()
        return total

    def __str__(self):
        return self.user.username

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    zip = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    country = CountryField(multiple=False)
    email = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.user.username},{self.city}'

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user  =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.SET_NULL,blank=True,null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username