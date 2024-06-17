from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    # path('verify-otp/', OTPVerificationView.as_view(), name='otp-verify'),
    path('update/<int:user_id>/', UserUpdateView.as_view(), name='user-update'),
    path('address', AddressListCreateView.as_view(), name='address-list-create'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),

]
