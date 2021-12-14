import json
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.testcases import SimpleTestCase
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Order, OrderDetails, Restaurant, Meal, Customer, Category
from .serializers import OrderSerializer

class CustomUserTests(TestCase):

    def test_create_user(self):
        user_model = get_user_model()
        user = user_model.objects.create_user(
            username='testUser',
            email="test@email.com",
            password="testpass123"
        )
        self.assertEqual(user.username, 'testUser')
        self.assertEqual(user.email, 'test@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        user_model = get_user_model()
        admin_user = user_model.objects.create_superuser(
            username='admin',
            email='admin@email.com',
            password='adminpass123'
        )
        self.assertEqual(admin_user.username, 'admin')
        self.assertEqual(admin_user.email, 'admin@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_superuser)


class HomepageTests(SimpleTestCase):
    pass


def set_up() -> dict:

    user = User.objects.create(username="testUser", password="testpass123")
    user_rest = User.objects.create(username="testUserRest", password="testpass123")

    customer= Customer.objects.create(
                                    user=user,
                                    address="test adress",
                                    phone="1234567890",
                                 )

  
    # create test category
    category = Category.objects.create(
                                    title="Test Category",
                                )
    # Create test restaurant
    restaurant = Restaurant.objects.create(
                                        user=user_rest,
                                        name="Test Restaurant",
                                        phone="01234567890",
                                        address="Test Adress",
                                        category=category
                                    )
    # create test meal
    meal = Meal.objects.create(
                            name="Test Meal",
                            restaurant=restaurant,
                            short_description="test desc",
                            price=40
                        )
    # create test order
    order_1 = Order.objects.create(
                            customer=customer,
                            restaurant=restaurant,
                            total=80,
                            status = Order.COOKING,
                        )
    order_2 = Order.objects.create(
                            customer=customer,
                            restaurant=restaurant,
                            total=80,
                            status= Order.DELIVERED
                        )
    invalid_order = Order.objects.create(
                                    customer=customer,
                                    restaurant=restaurant,
                                    total=100,
                                    status= Order.DELIVERED,

    )
    # create test order details
    order_details = OrderDetails.objects.create(
                                            order = order_1,
                                            meal = meal,
                                            quantity = 2,
                                            sub_total = 80
                                        )
    return {'valid':[order_1, order_2], 'invalid':[invalid_order]}


class TestOrdersList(APITestCase):

    def setUp(self) -> None:
        self.url = reverse("order-list")

        self.orders = set_up()
        self.serializer1 = OrderSerializer(self.orders['valid'][0])
        self.serializer2 = OrderSerializer(self.orders['valid'][1])

    def test_status_200(self):
        response = self.client.get(self.url)
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data, [self.serializer1.data, self.serializer2.data])


class TestOrderDetails(APITestCase):

    def setUp(self) -> None:
        self.orders = set_up()
        self.serializer = OrderSerializer(self.orders['valid'][0])

        self.url = reverse("order-details", args=[1, ])

    def test_list_valid(self):
        response = self.client.get(self.url)
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data, [self.serializer.data])

    def test_list_invalid(self):
        self.url = reverse("order-details", args=[30, ])
        response = self.client.get(self.url)
        self.assertTrue(response.status_code, status.HTTP_404_NOT_FOUND)

# class TestCreateOrder(APITestCase):
    
#     def setUp(self):
#         self.url = reverse("create-order")
#         self.orders = set_up()
    
#     def test_create_valid_order(self):
#         print(self.orders['valid'][0])
#         response = self.client.post(
#             self.url,
#             data=self.orders['valid'][0],
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
