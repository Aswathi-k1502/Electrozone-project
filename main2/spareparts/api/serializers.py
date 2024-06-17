from rest_framework import serializers
from .models import *
import random
import datetime
from django.contrib.auth.hashers import make_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'email', 'phone_number', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        otp = str(random.randint(100000, 999999))
        otp_created_at = datetime.datetime.now()

        user = User(
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            otp=otp,
            otp_created_at=otp_created_at
        )
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(max_length=10, required=False)
    password = serializers.CharField(max_length=100)

    def validate(self, data):
        email = data.get('email')
        phone_number = data.get('phone_number')
        if not email and not phone_number:
            raise serializers.ValidationError("Either email or phone number is required")
        return data

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    otp = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def save(self):
        email = self.validated_data['email']
        otp = self.validated_data['otp']
        new_password = self.validated_data['new_password']
        user = User.objects.get(email=email)

        if user.otp != otp:
            raise serializers.ValidationError("Invalid OTP.")

        # Hash the new password before saving
        user.password = new_password
        user.save()
        return user
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'firstname', 'lastname', 'email', 'phone_number']
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['vehicle_id', 'name', 'image']
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['brand_id', 'name', 'image']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'name', 'image']
class ModelYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelYear
        fields = ['modelyear_id', 'year']

class ProductSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(source='vehicle_id', read_only=True)  # Use source to point to vehicle_id ForeignKey
    brand = BrandSerializer(source='brand_id', read_only=True)
    category = CategorySerializer(source='category_id', read_only=True)
    modelyear = ModelYearSerializer(source='modelyear_id', read_only=True)

    class Meta:
        model = Product
        fields = ['product_id', 'title', 'image', 'price', 'vehicle', 'brand', 'highlights', 'description', 'category', 'modelyear', 'created_at']

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Cart
        fields = ['cart_id', 'product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer(source='cart_id', many=False)
    address = AddressSerializer(source='address_id', many=False)

    class Meta:
        model = Order
        fields = ['order_id', 'cart', 'address', 'user_id', 'total_amount', 'delivery_charges', 'coupon_discount', 'created_at']

class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['cart_id', 'address_id', 'user_id', 'total_amount', 'delivery_charges', 'coupon_discount']