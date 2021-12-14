from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='restaurant_logo', blank=False)

    def __str__(self):
        return str(self.id)+' '+self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    phone = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.id)+' '+self.user.get_full_name()


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
    phone = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)

    # class Meta:
    #     ordering = ['full_name']

    def __str__(self) -> str:
        return str(self.id)+' '+self.user.get_full_name()


class Category(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Meal', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    
    class Meta:
        verbose_name = "Categorie"
        ordering = ['title']

    def __str__(self) -> str:
        return self.title


class Meal(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    short_description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='meal_images/',blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return str(self.id)+' '+self.name


class Order(models.Model):
    COOKING = 1
    READY = 2
    ONTHEWAY = 3
    DELIVERED = 4

    STATUS_CHOICES =(
        (COOKING,"Cooking"),
        (READY,"Ready"),
        (ONTHEWAY,"On the way"),
        (DELIVERED,"Delivered"),
    )

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    restaurant = models.ForeignKey(Restaurant, models.PROTECT)
    driver = models.ForeignKey(Driver, models.PROTECT, blank=True, null=True)
    address = models.CharField(max_length=500)
    total = models.IntegerField()
    status = models.IntegerField(choices = STATUS_CHOICES)
    created_at = models.DateTimeField(default = timezone.now)
    picked_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.id)


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='order_details')
    meal = models.ForeignKey(Meal, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    sub_total = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = "Order Detail"

    def __str__(self):
        return str(self.id)

