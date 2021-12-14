from django.urls import path
from . import views
from . import apis
from . import unused_apis


urlpatterns = [
    # APIs for customers
    path('api/customer/restaurants/', unused_apis.customer_get_restaurants),
    path('api/customer/meals/<int:restaurant_id>/', unused_apis.customer_get_meals),
    path('api/customer/order/latest/', unused_apis.customer_get_latest_order),
    path('api/customer/driver/location/', unused_apis.customer_driver_location),
    # APIs for drivers
    path('api/driver/revenue/', unused_apis.driver_get_revenue),
    path('api/driver/location/update/', unused_apis.driver_update_location),

]