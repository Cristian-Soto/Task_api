from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()

class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    Endpoint para ver y actualizar el perfil de usuario actual
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class RegisterView(generics.CreateAPIView):
    """
    Endpoint para registrar nuevos usuarios
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
