"""
Buradaki kodlar daha sonra projeyi daha da geliştirmek için kullanılacak
"""

from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Customer, Restaurant, Meal, Order 
from .serializers import RestaurantSerializer, MealSerializer, OrderSerializer


@api_view()
def customer_get_restaurants(request):
    restaurants = RestaurantSerializer(
        Restaurant.objects.all().order_by("-id"),
        many = True,
        context = {"request":request}
    ).data

    return Response({"restaurants": restaurants})


@api_view()
def customer_get_meals(request, restaurant_id):
    meals = MealSerializer(
        Meal.objects.filter(restaurant_id = restaurant_id).order_by("-id"),
        many=True,
        context = {"request":request}
    ).data
    return Response({"meals": meals})


def customer_get_latest_order(request):
    # access_token = AccessToken.objects.get(token=request.GET.get("access_token"),expires__gt=timezone.now())
    # customer = access_token.user.customer
    customer = Customer.objects.get(id=request.GET.get("customer"))
    order = OrderSerializer(Order.objects.filter(customer = customer).last()).data
    return Response(order)


# GET params: access_token
def customer_driver_location(request):
    # access_token = AccessToken.objects.get(token=request.GET.get("access_token"),expires__gt=timezone.now())
    # customer = access_token.user.customer
    customer = Customer.objects.get(id=request.GET.get("customer"))

    # get driver's location related to this customer's order
    current_order = Order.objects.filter(customer = customer, status = Order.ONTHEWAY).last()
    location = current_order.driver.location

    return Response({"location": location})


###############
# RESTAURANTS #
###############

def restaurant_order_notification(request, last_request_time):
    """
        select count(*) from Orders
        where restaurant = request.user.restaurant AND created_at > last_request_time
    """
    notification = Order.objects.filter(restaurant = request.user.restaurant,
        created_at__gt = last_request_time).count()

    return Response({"notification":notification})


###########
# DRIVERS #
###########

# GET params: access_token
def driver_get_revenue(request):
    #access_token = AccessToken.objects.get(token=request.GET.get("access_token"),expires__gt=timezone.now())
    #driver = access_token.user.driver

    driver = request.GET.get("dri")
    revenue = {}
    today = timezone.now()
    current_weekdays = [today + timedelta(days=i) for i in range(0-today.weekday(), 7-today.weekday())]

    for day in current_weekdays:
        orders = Order.objects.filter(
            driver = driver,
            status = Order.DELIVERED,
            created_at__year = day.year,
            created_at__month = day.month,
            created_at__day = day.day,
        )

        revenue[day.strftime("%a")] = sum(order.total for order in orders)

    return Response({"revenue": revenue})


# POST params: access_token, 'lat', 'lng'
@csrf_exempt
def driver_update_location(request):
    if request.method == "POST":
        # access_token = AccessToken.objects.get(token=request.POST.get("access_token"),expires__gt=timezone.now())
        # driver = access_token.user.driver
        driver = request.POST.get("driver")

        # set location string -> database
        driver.location = request.POST["location"]
        driver.save()

        return Response({"status":"success"})