from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Task.
    
    Este serializador convierte las instancias del modelo Task a un formato JSON
    para el API REST y viceversa. Incluye todos los campos relevantes de la tarea
    y agrega un campo adicional para mostrar el texto descriptivo del estado.
    
    Attributes:
        status_display (str): Campo de solo lectura que muestra el texto descriptivo del estado
    """
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    username = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'status_display', 
            'created_at', 'user', 'username'
        ]
        read_only_fields = ['id', 'created_at', 'user', 'status_display', 'username']
    
    def validate_title(self, value):
        """
        Valida que el título de la tarea tenga al menos 5 caracteres.
        
        Args:
            value (str): El título a validar
            
        Returns:
            str: El título validado
            
        Raises:
            serializers.ValidationError: Si el título es muy corto
        """
        if len(value.strip()) < 5:
            raise serializers.ValidationError("El título debe tener al menos 5 caracteres.")
        return value