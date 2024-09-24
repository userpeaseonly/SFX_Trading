from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .models import OTP
from .serializers import OTPRequestSerializer, OTPVerifySerializer
from users.models import CustomUser

import random
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SignUpAPIView(APIView):
    
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=OTPRequestSerializer,
        responses={201: "User created successfully", 400: "User already exists"},
    )
    def post(self, request, *args, **kwargs):
        serializer = OTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        first_name = serializer.validated_data["first_name"]
        last_name = serializer.validated_data.get("last_name", "")
        telegram_id = serializer.validated_data["telegram_id"]

        user, created = CustomUser.objects.get_or_create(
            phone_number=phone_number,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "full_name": f"{first_name} {last_name}",
                "coins": 0,
                "telegram_id": telegram_id,
            },
        )
        if not created:
            return Response(
                {"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": "User created successfully"}, status=status.HTTP_201_CREATED
        )


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "telegram_id": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Telegram ID"
                )
            },
        ),
        responses={
            200: "OTP key generated",
            400: "telegram_id is required",
            404: "User does not exist",
        },
    )
    def post(self, request, *args, **kwargs):
        telegram_id = request.data.get("telegram_id")
        if not telegram_id:
            return Response(
                {"error": "telegram_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = CustomUser.objects.get(telegram_id=telegram_id)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        otp_key = f"{random.randint(100000, 999999)}"
        OTP.objects.create(user=user, key=otp_key)

        return Response({"otp_key": otp_key}, status=status.HTTP_200_OK)


class VerifyOTPAPIView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=OTPVerifySerializer,
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "refresh": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Refresh Token"
                    ),
                    "access": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Access Token"
                    ),
                },
            ),
            400: "Invalid OTP or OTP has expired",
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp_key = serializer.validated_data["otp_key"]

        try:
            otp_instance = OTP.objects.get(key=otp_key)
        except OTP.DoesNotExist:
            return Response(
                {"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
            )

        if otp_instance.is_expired():
            return Response(
                {"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = otp_instance.user
        refresh = RefreshToken.for_user(user)

        otp_instance.delete()

        return Response(
            {"refresh": str(refresh), "access": str(refresh.access_token)},
            status=status.HTTP_200_OK,
        )
