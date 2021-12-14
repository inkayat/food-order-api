import json
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import logging
from .models import Customer, Restaurant, Meal, Order, OrderDetails, Driver
from .serializers import RestaurantSerializer, MealSerializer, OrderSerializer

logger = logging.getLogger(__name__)

class OrderViewSet(ModelViewSet):
    """This is a ViewSet implementation for all Order functions
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_permission(self):
        if self.request.method in ['PATH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_queryset(self):
        return Order.objects.all()


@api_view()
def order_details(request, id):
    order = get_object_or_404(Order, pk=id)
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def order_list(request):
    if request.method == "GET":
        queryset = Order.objects.all()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST', 'GET'])
@csrf_exempt
def create_order(request):
    """
        params:
            access_token
            customer_id
            restaurant_id
            address
            order_details(json format),examples:
                [{"meal_id": 1, "quantity": 2},{"meal_id": 2, "quantity": 3}]
            stripe_token
        return:
            {"status":"success"}
    """
    try:
        if request.method == "POST":
            # # get token
            # access_token = AccessToken.objects.get(token = request.POST.get("access_token"),expires__gt = timezone.now())

            # #get Profile
            # customer = access_token.user.customer

            # # check whether customer has any order that is not DELIVERED
            # if Order.objects.filter(customer = customer).exclude(status = Order.DELIVERED):
            #     return Response({"status":"failed", "error":"Your last order must be completed"})

            # check address
            # if not request.POST["address"]:
            #     return Response({"status":"failed", "error":"Address is required"})

            # get order details
            order_details = json.loads(request.POST["order_details"])

            order_total = 0
            for meal in order_details:
                order_total += Meal.objects.get(id=meal["meal_id"]).price * meal["quantity"]
            if len(order_details)>0:
                stat = "success"
                if stat != "failed":
                    # step 2: create an order
                    order = Order.objects.create(
                        customer = Customer.objects.get(id=request.POST["customer_id"]),
                        restaurant_id = request.POST["restaurant_id"],
                        total = order_total,
                        status = Order.COOKING,
                        address = request.POST["address"]
                    )
                    # step 3: create order details
                    for meal in order_details:
                        OrderDetails.objects.create(
                            order = order,
                            meal_id = meal["meal_id"],
                            quantity = meal["quantity"],
                            sub_total = Meal.objects.get(id=meal["meal_id"]).price * meal["quantity"]
                        )
                    return Response({"status":"success"}, status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        raise e("Order create failed!")

    else:
        return Response({"status":"Failed"})    


###########
# DRIVERS #
###########

@api_view()
def driver_get_ready_orders(request):
    orders = OrderSerializer(
        Order.objects.filter(status=Order.READY, driver=None).order_by("-id"),
        many=True
    ).data

    return Response({"orders":orders})


@api_view(['GET', 'POST'])
@csrf_exempt
# POST params: access_token, order_id, driver_id
def driver_pick_order(request):
    if request.method == "POST":
        # get token
        # access_token = AccessToken.objects.get(token=request.POST.get("access_token"),expires__gt=timezone.now())
        # get driver
        # driver = access_token.user.driver
        # check whether driver can only pick one order at the same time
        driver_id = request.POST.get("driver_id")

        driver = Driver.objects.get(id=driver_id)

        if Order.objects.filter(driver=driver).exclude(status=Order.ONTHEWAY):
            return Response({"status":"failed", "error": "You can only pick one order at the same time."})
        try:
            order = Order.objects.get(
                id = request.POST["order_id"],
                driver = None,
                status = Order.READY
            )
            order.driver = driver
            order.status = Order.ONTHEWAY
            order.picked_at = timezone.now()
            order.save()

            return Response({"status":"success"})

        except Order.DoesNotExist:
            return Response({"status":"failed", "error":"This order has been picked up by another."})
    return Response({})


# GET params: access_token
def driver_get_latest_order(request):
    driver = request.GET.get("driver")

    order = OrderSerializer(
        Order.objects.filter(driver = driver).order_by("picked_at").last()
    ).data

    return Response({"order": order}, status=status.HTTP_200_OK)


# POST params: access_token, order_id
@api_view(['GET', 'POST'])
@csrf_exempt
def driver_complete_order(request):

    driver_id = request.POST.get("driver_id")
    order_id = request.POST.get("order_id")

    order = Order.objects.get(
        id = order_id,
        driver = Driver.objects.get(id=driver_id)
    )
    order.status = Order.DELIVERED
    order.save()
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)