from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'status_display', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'user', 'status_display']