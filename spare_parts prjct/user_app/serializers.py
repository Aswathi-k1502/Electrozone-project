from rest_framework import serializers
from .models import *
import random
from django.utils import timezone
from twilio.rest import Client
from django.conf import settings

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'mobile_number', 'password']

# class OTPVerificationSerializer(serializers.Serializer):
#     mobile_number = serializers.CharField(max_length=10)
#     otp = serializers.CharField(max_length=6)
class UserLoginSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=10)
    password = serializers.CharField(max_length=100)

class UserupdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'mobile_number', 'password', 'is_active']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address_id', 'user_id', 'fullname', 'phone_number', 'address', 'pin_code', 'state', 'city', 'landmark']


# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['product_id', 'title', 'image', 'price', 'vehicle', 'highlights', 'description', 'category', 'year', 'created_at']

# class OrderSerializer(serializers.ModelSerializer):
#     user_id = UserRegistrationSerializer()
#     product_id = ProductSerializer()
#     address_id = AddressSerializer()
#
#     class Meta:
#         model = Order
#         fields = ['order_id', 'user_id', 'product_id', 'address_id', 'quantity', 'total', 'payment_method']
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 'user_id', 'product_id', 'address_id', 'quantity', 'total', 'payment_method']
