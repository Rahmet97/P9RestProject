"""
URL configuration for RestAPIProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from accounts.views import ResetPasswordAPIView, PasswordResetConfirmAPIView

router = routers.DefaultRouter()
schema_view = get_swagger_view(title="API Documentation")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("api.urls")),
    path('accounts/', include("accounts.urls")),
    path('docs/', schema_view),
    path('paycom/', include("paycom.urls")),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/password/reset/', ResetPasswordAPIView.as_view(), name='password-reset'),
    path('api/password/reset/<str:token>/<str:uuid>/', PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),
]
