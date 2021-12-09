from django.urls import path
from . import views

urlpatterns = [
    path('/', views.restaurant_home, name='restaurant-home'),
    path('home/', views.home, name='home'),
]