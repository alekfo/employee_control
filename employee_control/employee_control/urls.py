"""
URL configuration for employee_control project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from employees.views import EmployeeViewSet

router = DefaultRouter()
#DefaultRouter анализирует EmployeeViewSet и автоматически генерирует набор URL-маршрутов:
#/employees/ → для list и create (GET, POST)
#/employees/{id}/ → для retrieve, update, partial_update, destroy (GET, PUT, PATCH, DELETE)
router.register(r'employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #принимает username и password, возвращает access и refresh токены.
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #принимает refresh токен, возвращает новый access токен.
]