from django import forms

from django.contrib.auth.models import User
from yemeksepetiapp.models import Restaurant

class UserForm(forms.ModelForm):
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ("name", "phone", "address")