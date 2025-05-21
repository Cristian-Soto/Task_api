from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics, filters, status
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer

@api_view(['GET'])
def hello_world(request):
    """
    Vista simple para verificar que la API está funcionando.
    
    Returns:
        JsonResponse: Mensaje de saludo
    """
    return JsonResponse({"message": "¡Bienvenido a la API de Gestión de Tareas!"})

class TaskListCreateView(generics.ListCreateAPIView):
    """
    API endpoint que permite listar todas las tareas del usuario autenticado
    y crear nuevas tareas.
    
    Métodos soportados:
    * GET: Obtener lista de tareas
    * POST: Crear una nueva tarea
    
    El filtrado de tareas se realiza automáticamente según el usuario autenticado,
    mostrando solo las tareas que le pertenecen.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'status', 'title']
    ordering = ['-created_at']  # Ordenar por fecha de creación descendente por defecto
    
    def get_queryset(self):
        """Retorna las tareas del usuario autenticado."""
        user = self.request.user
        return Task.objects.filter(user=user)

    def perform_create(self, serializer):
        """Asigna el usuario autenticado como propietario de la tarea."""
        serializer.save(user=self.request.user)
        
    def list(self, request, *args, **kwargs):
        """Lista las tareas con información adicional sobre conteo por estado."""
        queryset = self.filter_queryset(self.get_queryset())
        
        # Contar tareas por estado
        pending_count = queryset.filter(status=Task.STATUS_PENDING).count()
        in_progress_count = queryset.filter(status=Task.STATUS_IN_PROGRESS).count()
        completed_count = queryset.filter(status=Task.STATUS_COMPLETED).count()
        
        # Serializar y devolver la respuesta
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            response = Response(serializer.data)
        
        # Añadir metadatos
        response.data['meta'] = {
            'total_count': queryset.count(),
            'pending_count': pending_count,
            'in_progress_count': in_progress_count,
            'completed_count': completed_count
        }
        
        return response


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint que permite realizar operaciones sobre una tarea específica.
    
    Métodos soportados:
    * GET: Obtener detalles de una tarea
    * PUT/PATCH: Actualizar una tarea
    * DELETE: Eliminar una tarea
    
    Sólo se puede acceder a las tareas que pertenecen al usuario autenticado.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Retorna sólo las tareas pertenecientes al usuario autenticado para
        garantizar que un usuario no pueda acceder a las tareas de otros.
        """
        return Task.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        """
        Personaliza la respuesta al actualizar una tarea.
        
        Returns:
            Response: Respuesta con los datos de la tarea actualizada y un mensaje de éxito
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'status': 'success',
            'message': 'Tarea actualizada correctamente',
            'data': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        """
        Personaliza la respuesta al eliminar una tarea.
        
        Returns:
            Response: Respuesta con mensaje de éxito
        """
        instance = self.get_object()
        task_id = instance.id
        task_title = instance.title
        self.perform_destroy(instance)
        
        return Response({
            'status': 'success',
            'message': f'Tarea "{task_title}" (ID: {task_id}) eliminada correctamente'
        }, status=status.HTTP_200_OK)
