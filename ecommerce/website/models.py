from django.db import models
from django.conf import settings
from django_mysql.models import ListCharField
from django.shortcuts import reverse

STATUS_CHOICES = (
    ('N',''),
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


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete= models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username



