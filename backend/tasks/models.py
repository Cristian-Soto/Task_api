from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Task(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pendiente'),
        (STATUS_IN_PROGRESS, 'En proceso'),
        (STATUS_COMPLETED, 'Completada'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        app_label = 'tasks'

    def __str__(self):
        return self.title