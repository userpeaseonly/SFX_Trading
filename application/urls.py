import os

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions



schema_view = get_schema_view(
    openapi.Info(
        title="SFX Trading Center API",
        default_version='v1',
        description="API description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
    url=os.environ.get('HTTP_URL'),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('otp/', include('otp.urls')),
    path('tasks/', include('tasks.urls')),
    path('i18n/', include('django.conf.urls.i18n')), 
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
