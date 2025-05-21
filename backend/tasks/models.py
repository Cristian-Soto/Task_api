from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Task(models.Model):
    """
    Modelo que representa una tarea en el sistema.
    
    Este modelo almacena la información relevante de las tareas, incluyendo su título,
    descripción, estado actual, fecha de creación y el usuario al que pertenece.
    
    Attributes:
        title (str): Título descriptivo de la tarea
        description (str): Descripción detallada de la tarea (opcional)
        status (str): Estado actual de la tarea (pendiente, en proceso, completada)
        created_at (datetime): Fecha y hora de creación de la tarea
        user (ForeignKey): Usuario propietario de la tarea
    """
    # Constantes para los estados de las tareas
    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pendiente'),
        (STATUS_IN_PROGRESS, 'En proceso'),
        (STATUS_COMPLETED, 'Completada'),
    ]
    
    title = models.CharField(max_length=255, verbose_name="Título")
    description = models.TextField(blank=True, verbose_name="Descripción")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name="Estado"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Usuario"
    )

    class Meta:
        app_label = 'tasks'
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering = ['-created_at']  # Ordenar por fecha de creación descendente

    def __str__(self):
        """Representación en cadena de texto del objeto."""
        return self.title
    
    @property
    def is_completed(self):
        """Indica si la tarea está completada o no."""
        return self.status == self.STATUS_COMPLETED
    
    @property
    def is_in_progress(self):
        """Indica si la tarea está en proceso o no."""
        return self.status == self.STATUS_IN_PROGRESS
    
    def start_task(self):
        """Marca la tarea como 'en proceso'."""
        if self.status == self.STATUS_PENDING:
            self.status = self.STATUS_IN_PROGRESS
            self.save(update_fields=['status'])
    
    def complete_task(self):
        """Marca la tarea como 'completada'."""
        self.status = self.STATUS_COMPLETED
        self.save(update_fields=['status'])