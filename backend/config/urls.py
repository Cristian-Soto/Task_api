from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

def home_view(request):
    return JsonResponse({"message": "Bienvenido a la API. Usa /api/token/ para autenticación."})

# Configuración de Swagger UI
schema_view = get_schema_view(
    openapi.Info(
        title="Task API",
        default_version="v1",
        description="""
        API para la gestión de tareas.
        
        ## Autenticación
        
        Para usar esta API, necesitas autenticarte siguiendo estos pasos:
        
        1. Usa el endpoint `/api/token/` para obtener un token JWT con tu usuario y contraseña.
        2. Copia el valor del campo "access" en la respuesta.
        3. En cada solicitud a la API, incluye un encabezado HTTP: `Authorization: Bearer tu_token_aquí`.
        
        Ejemplo de solicitud para obtener token:
        ```
        POST /api/token/
        Content-Type: application/json
        
        {
            "email": "tu_email@email.com",
            "password": "tu_contraseña"
        }
        ```
        
        Ejemplo de uso del token:
        ```
        GET /api/tasks/
        Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
        ```
        """,
        
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', home_view),
    path('api/tasks/', include('backend.tasks.urls')),
    path('api/', include('backend.users.urls')),  # Nuevos endpoints de usuario
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
