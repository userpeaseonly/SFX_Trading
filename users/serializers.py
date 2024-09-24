from rest_framework import serializers
from .models import CustomUser

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'first_name', 'last_name', 'full_name', 'email', 'telegram_id', 'profile_image', 'coins']
        read_only_fields = ['id', 'full_name', 'coins']
