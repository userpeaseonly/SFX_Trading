from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class OTPRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField(required=False, allow_blank=True)
    telegram_id = serializers.CharField()

class OTPVerifySerializer(serializers.Serializer):
    otp_key = serializers.CharField()
