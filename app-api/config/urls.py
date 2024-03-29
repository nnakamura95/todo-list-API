"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

api_v1 = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{api_v1}', include('app.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path(f'{api_v1}user/', include('user.urls')),
    path(f'{api_v1}login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
