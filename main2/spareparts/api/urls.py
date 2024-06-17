from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('users/', list_users, name='user-list'),
    path('user_get/<int:user_id>/', user_detail_get, name='user-detail_get'),
    path('user_update/<int:user_id>/', user_detail_update, name='user-detail_update'),
    path('user_delete/<int:user_id>/', user_detail_delete, name='user-detail_delete'),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    path('address/', list_addresses, name='list-addresses'),
    path('address_create/', create_address, name='create-address'),
    path('address/<int:address_id>/', get_address, name='get-address'),
    path('addresses_update/<int:address_id>/', update_address, name='update-address'),
    path('addresses_delete/<int:address_id>/', delete_address, name='delete-address'),
    path('vehicle/<int:vehicle_id>/', products_by_vehicle, name='products_by_vehicle'),
    path('brand/<int:brand_id>/', products_by_brand, name='products_by_brand'),
    path('category/<int:category_id>/', products_by_category, name='products_by_category'),
    path('modelyear/<int:modelyear_id>/', products_by_modelyear, name='products_by_modelyear'),
    path('orders/<int:user_id>/', get_user_orders, name='get-user-orders'),
    path('orders_create/', create_order, name='create-order'),
    path('api/orders_delete/<str:order_id>/', delete_order, name='delete-order'),
]
