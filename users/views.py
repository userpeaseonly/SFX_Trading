from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import CustomUser
from .serializers import UserInfoSerializer

class UserExistsAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('telegram_id', openapi.IN_QUERY, description="Telegram ID", type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'exists': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='User existence flag')
            }
        )}
    )
    def get(self, request, *args, **kwargs):
        telegram_id = request.query_params.get('telegram_id')
        if not telegram_id:
            return Response({"exists": False}, status=status.HTTP_400_BAD_REQUEST)
        
        user = CustomUser.objects.filter(telegram_id=telegram_id)
        
        user_exists = user.exists()
        
        return Response({"exists": user_exists, "user_id": user.first().id if user_exists else -1}, status=status.HTTP_200_OK)


class UserInfoAPIView(generics.RetrieveAPIView):
    serializer_class = UserInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
