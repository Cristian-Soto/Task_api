# filepath: d:\task_api\backend\tasks\serializers.py
from rest_framework import serializers
from django.utils import timezone
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Task.
    
    Este serializador convierte las instancias del modelo Task a un formato JSON
    para el API REST y viceversa. Incluye todos los campos relevantes de la tarea
    y agrega campos adicionales para mejorar la experiencia de usuario.
    
    Attributes:
        status_display (str): Campo de solo lectura que muestra el texto descriptivo del estado
        priority_display (str): Campo de solo lectura que muestra el texto descriptivo de la prioridad
        username (str): Campo de solo lectura que muestra el nombre del usuario propietario
        is_overdue (bool): Campo calculado que indica si la tarea está vencida
        days_remaining (int): Campo calculado con los días restantes hasta la fecha límite
    """
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    username = serializers.ReadOnlyField(source='user.username')
    is_overdue = serializers.SerializerMethodField(read_only=True)
    days_remaining = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'status_display', 
            'priority', 'priority_display', 'created_at', 'due_date', 
            'is_overdue', 'days_remaining', 'user', 'username'
        ]
        read_only_fields = ['id', 'created_at', 'user', 'status_display', 
                            'priority_display', 'username', 'is_overdue', 'days_remaining']
    
    def get_is_overdue(self, obj):
        """
        Calcula si la tarea está vencida comparando la fecha límite con la fecha actual.
        
        Args:
            obj (Task): Instancia del modelo de tarea
            
        Returns:
            bool: True si la fecha límite ha pasado y la tarea no está completada, False en caso contrario
        """
        if obj.due_date and obj.status != Task.STATUS_COMPLETED:
            return timezone.now() > obj.due_date
        return False
    
    def get_days_remaining(self, obj):
        """
        Calcula los días restantes hasta la fecha límite.
        
        Args:
            obj (Task): Instancia del modelo de tarea
            
        Returns:
            int: Número de días hasta la fecha límite, o None si no hay fecha límite
        """
        if obj.due_date:
            delta = obj.due_date - timezone.now()
            return delta.days if delta.days >= 0 else 0
        return None
    
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
        
    def validate_due_date(self, value):
        """
        Valida que la fecha límite sea en el futuro.
        
        Args:
            value (datetime): La fecha límite a validar
            
        Returns:
            datetime: La fecha límite validada
            
        Raises:
            serializers.ValidationError: Si la fecha límite está en el pasado
        """
        if value and value < timezone.now():
            raise serializers.ValidationError("La fecha límite debe ser una fecha futura.")
        return value
        
    def validate_priority(self, value):
        """
        Valida que la prioridad sea una de las opciones permitidas.
        
        Args:
            value (str): La prioridad a validar
            
        Returns:
            str: La prioridad validada
            
        Raises:
            serializers.ValidationError: Si la prioridad no es válida
        """
        valid_priorities = dict(Task.PRIORITY_CHOICES).keys()
        if value not in valid_priorities:
            raise serializers.ValidationError(f"La prioridad debe ser una de las siguientes: {', '.join(valid_priorities)}")
        return value
