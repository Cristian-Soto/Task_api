from django.urls import path
from .views import UserDetailView, RegisterView

urlpatterns = [
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('users/me/', UserDetailView.as_view(), name='user-me'),  # Nuevo endpoint para /users/me/
    path('register/', RegisterView.as_view(), name='register'),
]