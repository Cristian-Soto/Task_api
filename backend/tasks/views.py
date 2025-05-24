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
    
    Filtros disponibles:
    * status: Filtrar por estado (pending, in_progress, completed)
    * priority: Filtrar por prioridad (low, medium, high)
    * has_due_date: Filtrar tareas con fecha límite (true, false)
    * is_overdue: Filtrar tareas vencidas (true, false) 
    * due_date_before: Filtrar tareas con fecha límite anterior a una fecha (YYYY-MM-DD)
    * due_date_after: Filtrar tareas con fecha límite posterior a una fecha (YYYY-MM-DD)
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'status', 'priority', 'title', 'due_date']
    ordering = ['-created_at']  # Ordenar por fecha de creación descendente por defecto
    
    def get_queryset(self):
        """
        Retorna las tareas del usuario autenticado.
        
        Aplica filtros adicionales basados en parámetros de consulta:
        - status: Filtra por estado de tarea
        - priority: Filtra por prioridad de tarea
        - has_due_date: Filtra tareas con/sin fecha límite
        - is_overdue: Filtra tareas vencidas/no vencidas
        - due_date_before: Filtra tareas con fecha límite antes de la fecha especificada
        - due_date_after: Filtra tareas con fecha límite después de la fecha especificada
        """
        from django.utils import timezone
        from datetime import datetime
        from django.db.models import Q
        
        user = self.request.user
        queryset = Task.objects.filter(user=user)
        
        # Filtro por estado
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        # Filtro por prioridad
        priority = self.request.query_params.get('priority', None)
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Filtro por presencia de fecha límite
        has_due_date = self.request.query_params.get('has_due_date', None)
        if has_due_date is not None:
            has_due = has_due_date.lower() == 'true'
            if has_due:
                queryset = queryset.filter(due_date__isnull=False)
            else:
                queryset = queryset.filter(due_date__isnull=True)
        
        # Filtro por tareas vencidas
        is_overdue = self.request.query_params.get('is_overdue', None)
        if is_overdue is not None:
            is_over = is_overdue.lower() == 'true'
            now = timezone.now()
            if is_over:
                queryset = queryset.filter(
                    due_date__lt=now,
                    status__in=[Task.STATUS_PENDING, Task.STATUS_IN_PROGRESS]
                )
            else:
                queryset = queryset.filter(
                    Q(due_date__gte=now) | Q(status=Task.STATUS_COMPLETED) | Q(due_date__isnull=True)
                )
        
        # Filtros por rango de fecha
        due_date_before = self.request.query_params.get('due_date_before', None)
        if due_date_before:
            try:
                date = datetime.strptime(due_date_before, '%Y-%m-%d').date()
                queryset = queryset.filter(due_date__date__lte=date)
            except ValueError:
                pass  # Ignorar valores de fecha inválidos
        
        due_date_after = self.request.query_params.get('due_date_after', None)
        if due_date_after:
            try:
                date = datetime.strptime(due_date_after, '%Y-%m-%d').date()
                queryset = queryset.filter(due_date__date__gte=date)
            except ValueError:
                pass  # Ignorar valores de fecha inválidos
                
        return queryset

    def perform_create(self, serializer):
        """Asigna el usuario autenticado como propietario de la tarea."""
        serializer.save(user=self.request.user)
        
    def list(self, request, *args, **kwargs):
        """Lista las tareas con información adicional sobre conteo por estado y prioridad."""
        queryset = self.filter_queryset(self.get_queryset())
        
        # Contar tareas por estado
        pending_count = queryset.filter(status=Task.STATUS_PENDING).count()
        in_progress_count = queryset.filter(status=Task.STATUS_IN_PROGRESS).count()
        completed_count = queryset.filter(status=Task.STATUS_COMPLETED).count()
        
        # Contar tareas por prioridad
        low_priority_count = queryset.filter(priority=Task.PRIORITY_LOW).count()
        medium_priority_count = queryset.filter(priority=Task.PRIORITY_MEDIUM).count()
        high_priority_count = queryset.filter(priority=Task.PRIORITY_HIGH).count()
        
        # Serializar y devolver la respuesta
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            response = Response(serializer.data)
        
        # Añadir metadatos
        from django.utils import timezone
        now = timezone.now()
        
        # Contar tareas vencidas
        overdue_count = queryset.filter(
            due_date__lt=now,
            status__in=[Task.STATUS_PENDING, Task.STATUS_IN_PROGRESS]
        ).count()
        
        # Contar tareas con fecha límite
        tasks_with_due_date = queryset.filter(due_date__isnull=False).count()
        
        response.data['meta'] = {
            'total_count': queryset.count(),
            'status_counts': {
                'pending_count': pending_count,
                'in_progress_count': in_progress_count,
                'completed_count': completed_count,
            },
            'priority_counts': {
                'low_count': low_priority_count,
                'medium_count': medium_priority_count,
                'high_count': high_priority_count,
            },
            'overdue_count': overdue_count,
            'tasks_with_due_date': tasks_with_due_date
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
