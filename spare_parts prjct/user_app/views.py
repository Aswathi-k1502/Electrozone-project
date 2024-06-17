from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from django.utils import timezone
from twilio.rest import Client
from django.conf import settings
from spare_part_app.serializers import *


def send_otp(mobile_number, otp):
    # Ensure the phone number is in E.164 format for India
    if not mobile_number.startswith('+91'):
        mobile_number = '+91' + mobile_number.lstrip('0')  # Remove leading zero if present
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP is {otp}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=mobile_number
    )
    return message.sid


class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            otp = str(random.randint(100000, 999999))
            mobile_number = serializer.validated_data['mobile_number']
            try:
                send_otp(mobile_number, otp)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            user = User(
                name=serializer.validated_data['name'],
                mobile_number=mobile_number,
                password=serializer.validated_data['password'],
                otp=otp,
                otp_created_at=timezone.now()
            )
            user.save()
            return Response({"message": "OTP sent to your mobile number"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class OTPVerificationView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = OTPVerificationSerializer(data=request.data)
#         if serializer.is_valid():
#             mobile_number = serializer.validated_data['mobile_number']
#             otp = serializer.validated_data['otp']
#
#             try:
#                 user = User.objects.get(mobile_number=mobile_number, otp=otp)
#                 time_diff = timezone.now() - user.otp_created_at
#                 if time_diff.total_seconds() > 300:  # OTP is valid for 5 minutes
#                     return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
#
#                 user.otp = None
#                 user.otp_created_at = None
#                 user.is_active = True
#                 user.save()
#                 return Response({"message": "User registered successfully"}, status=status.HTTP_200_OK)
#             except User.DoesNotExist:
#                 return Response({"error": "Invalid OTP or mobile number"}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            mobile_number = serializer.validated_data['mobile_number']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(mobile_number=mobile_number)
                if check_password(password, user.password):
                    return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(APIView):
    def put(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserupdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddressListCreateView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
