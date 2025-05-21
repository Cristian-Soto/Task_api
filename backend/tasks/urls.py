from django.urls import path
from .views import TaskListCreateView, TaskRetrieveUpdateDestroyView, hello_world

# Definición de rutas para la API de tareas
urlpatterns = [
    # Endpoint para listar todas las tareas y crear nuevas tareas
    path('', TaskListCreateView.as_view(), name='task-list-create'),
    
    # Endpoint para obtener, actualizar y eliminar una tarea específica
    path('<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),
    
    # Endpoint de bienvenida/prueba
    path('hello/', hello_world, name='hello_world'),
]

# Si se añaden más patrones de URL, documentarlos adecuadamente