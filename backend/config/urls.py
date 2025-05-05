from django.contrib import admin
from django.urls import path
from django.http import JsonResponse 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

def home_view(request):
    return JsonResponse({"message": "Bienvenido a la API. Usa /api/token/ para autenticación."})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', home_view),
]
