from django.contrib import admin

from .models import OrderDetails, Restaurant, Category, Customer, Driver, Meal, Order

admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(Meal)
admin.site.register(Order)
admin.site.register(OrderDetails)