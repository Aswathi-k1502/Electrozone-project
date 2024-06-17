from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from .serializers import *
from .models import *
from django.shortcuts import get_object_or_404


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Send OTP email
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {user.otp}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return Response({"message": "OTP sent to email."},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            phone_number = serializer.validated_data.get('phone_number')
            password = serializer.validated_data.get('password')

            try:
                if email:
                    user = User.objects.get(email=email)
                elif phone_number:
                    user = User.objects.get(phone_number=phone_number)
                else:
                    return Response({'error': 'Email or phone number required'}, status=status.HTTP_400_BAD_REQUEST)


                if user.password != password:
                    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

                # Set user_id in session
                request.session['user_id'] = user.user_id

                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ChangePasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                otp = str(random.randint(100000, 999999))
                user.otp = otp
                user.otp_created_at = datetime.datetime.now()
                user.save()

                # Send OTP email
                send_mail(
                    'Your OTP Code for Password Change',
                    f'Your OTP code is {otp}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )

                return Response({"message": "OTP sent to email."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
            except serializers.ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    def post(self, request):
        # Clear the session data
        request.session.flush()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
@api_view(['GET'])
def list_users(request):
    users = User.objects.all()
    serializer = UserDetailSerializer(users, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def user_detail_get(request, user_id):
    user = User.objects.get(user_id=user_id)
    if request.method == 'GET':
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

@api_view([ 'PUT'])
def user_detail_update(request, user_id):
    user = User.objects.get(user_id=user_id)
    if request.method == 'PUT':
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def user_detail_delete(request, user_id):
    user = User.objects.get(user_id=user_id)
    if request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

####################################################address##################################################
@api_view(['GET'])
def list_addresses(request):
    addresses = Address.objects.all()
    serializer = AddressSerializer(addresses, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_address(request):
    if request.method == 'POST':
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_address(request, address_id):
    address = Address.objects.get(pk=address_id)
    serializer = AddressSerializer(address)
    return Response(serializer.data)


@api_view(['PUT'])
def update_address(request, address_id):
    try:
        address = Address.objects.get(pk=address_id)
    except Address.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_address(request, address_id):
    address = Address.objects.get(pk=address_id)
    if request.method == 'DELETE':
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#################################################filter section####################################################

@api_view(['GET'])
def products_by_vehicle(request, vehicle_id):
    try:
        products = Product.objects.filter(vehicle_id=vehicle_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({"message": "Products not found for this vehicle"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def products_by_brand(request, brand_id):
    try:
        products = Product.objects.filter(brand_id=brand_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({"message": "Products not found for this brand"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def products_by_category(request, category_id):
    try:
        products = Product.objects.filter(category_id=category_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({"message": "Products not found for this category"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def products_by_modelyear(request, modelyear_id):
    try:
        products = Product.objects.filter(modelyear_id=modelyear_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({"message": "Products not found for this model_year"}, status=status.HTTP_404_NOT_FOUND)

####################################order#####################################################
@api_view(['GET'])
def get_user_orders(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    orders = Order.objects.filter(user_id=user)
    if not orders.exists():
        return Response({'message': 'No orders found for this user'}, status=status.HTTP_200_OK)

    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['POST'])
def create_order(request):
    serializer = CreateOrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_order(request, order_id):
    order = Order.objects.get(order_id=order_id)
    order.delete()
    return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)