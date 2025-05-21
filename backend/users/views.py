from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()

class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    Endpoint para ver y actualizar el perfil de usuario actual.
    
    Métodos soportados:
    * GET: Obtener información del perfil del usuario autenticado
    * PUT/PATCH: Actualizar información del perfil del usuario autenticado
    
    Este endpoint está protegido y solo es accesible para usuarios autenticados.
    El usuario solo puede ver y modificar su propio perfil.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Retorna el usuario autenticado actualmente."""
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        """
        Personaliza la respuesta al obtener los detalles del usuario.
        
        Returns:
            Response: Datos del usuario con mensaje de éxito
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status': 'success',
            'message': 'Perfil de usuario recuperado correctamente',
            'data': serializer.data
        })
    
    def update(self, request, *args, **kwargs):
        """
        Personaliza la respuesta al actualizar el perfil del usuario.
        
        Returns:
            Response: Datos actualizados del usuario con mensaje de éxito
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'status': 'success',
            'message': 'Perfil actualizado correctamente',
            'data': serializer.data
        })


class RegisterView(generics.CreateAPIView):
    """
    Endpoint para registrar nuevos usuarios en el sistema.
    
    Método soportado:
    * POST: Crear un nuevo usuario
    
    Este endpoint es público y permite a cualquier persona registrarse en el sistema.
    Requiere proporcionar un nombre de usuario único, correo electrónico y contraseña.
    La contraseña debe cumplir con los requisitos de seguridad establecidos.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        """
        Personaliza la respuesta al crear un nuevo usuario.
        
        Returns:
            Response: Datos del usuario creado con mensaje de éxito
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            'status': 'success',
            'message': 'Usuario registrado correctamente. Ya puede iniciar sesión.',
            'data': {
                'id': serializer.instance.id,
                'username': serializer.instance.username,
                'email': serializer.instance.email
            }
        }, status=status.HTTP_201_CREATED)
