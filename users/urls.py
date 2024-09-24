from django.urls import path
from .views import UserExistsAPIView, UserInfoAPIView

urlpatterns = [
    path('user_exists_info/', UserExistsAPIView.as_view(), name='user_exists_info'),
    path('user_info/', UserInfoAPIView.as_view(), name='user_info'),
]
