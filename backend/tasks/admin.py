from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    """
    Configuración del administrador para el modelo Task.
    
    Permite una gestión eficiente de las tareas desde el panel de administración
    de Django, con filtros, campos de búsqueda y visualización personalizados.
    """
    list_display = ('title', 'status', 'priority', 'user', 'created_at', 'due_date')
    list_filter = ('status', 'priority', 'created_at', 'due_date')
    search_fields = ('title', 'description', 'user__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    # Personalizar los filtros de fecha
    list_per_page = 20
    
    # Campos de solo lectura
    readonly_fields = ('created_at',)
    
    # Campos para la creación/edición
    fieldsets = (
        ('Información básica', {
            'fields': ('title', 'description', 'status', 'priority')
        }),
        ('Asignación', {
            'fields': ('user',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'due_date')
        }),
    )

# Registrar el modelo con su configuración personalizada
admin.site.register(Task, TaskAdmin)
