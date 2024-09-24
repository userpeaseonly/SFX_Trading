from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView as RefreshToken
from .views import SignUpAPIView, LoginAPIView, VerifyOTPAPIView

urlpatterns = [
    path('sign_up/', SignUpAPIView.as_view(), name='otp_sign_up'),
    path('login/', LoginAPIView.as_view(), name='otp_login'),
    path('verify/', VerifyOTPAPIView.as_view(), name='otp_verify'),
    path('token/refresh/', RefreshToken.as_view(), name='token_refresh'),
]
