# 🐍 Django REST API - Sistema de Gestión de Tareas

[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![DRF](https://img.shields.io/badge/DRF-3.14-red.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Un sistema de gestión de tareas **robusto y escalable** implementado como API RESTful, construido con Django y Django REST Framework. La aplicación proporciona una plataforma completa para gestionar tareas con múltiples estados, prioridades, autenticación segura, y una API bien documentada.

> 🌟 **Características destacadas**: Estados de tareas personalizados (pendiente, en proceso, completada), prioridades de tareas (baja, media, alta), autenticación JWT, documentación interactiva con Swagger, y containerización con Docker.

![System Architecture](https://via.placeholder.com/800x400?text=Task+API+Architecture)

---

## 🚀 Tecnologías utilizadas

- Python 3.12
- Django 5.2
- Django REST Framework
- PostgreSQL
- JWT para autenticación
- Docker & Docker Compose
- Swagger/OpenAPI para documentación

---

## 📋 Requisitos previos

- Docker y Docker Compose instalados
- Git (opcional, para clonar el repositorio)
- Postman o similar (opcional, para probar la API)

## ⚙️ Configuración e instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/task_api.git
cd task_api
```

### 2. Configuración del entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Configuración de Django
SECRET_KEY=tu_clave_secreta_aqui
DEBUG=True

# Configuración de la base de datos PostgreSQL
POSTGRES_DB=taskapi
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### 3. Iniciar los contenedores Docker

```bash
docker-compose up -d
```

Este comando construirá las imágenes necesarias e iniciará los contenedores de Django y PostgreSQL. La API estará disponible en `http://localhost:8000`.

### 4. Aplicar migraciones y cargar datos iniciales

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py loaddata initial_data.json
```

### 5. Crear un superusuario (opcional)

```bash
docker-compose exec web python manage.py createsuperuser
```

Sigue las instrucciones para crear un superusuario que te permitirá acceder al panel de administración en `http://localhost:8000/admin/`.

### Configuración para desarrollo local (sin Docker)

Si prefieres desarrollar sin Docker:

```bash
# 1. Crear y activar entorno virtual
python -m venv venv
.\venv\Scripts\Activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar SQLite para desarrollo local
# (Editar backend/config/settings.py si es necesario)

# 4. Aplicar migraciones
python manage.py migrate

# 5. Ejecutar servidor de desarrollo
python manage.py runserver
```

---

## 🔑 Autenticación

La API utiliza autenticación JWT (JSON Web Token). Para acceder a los endpoints protegidos, necesitas:

1. **Obtener un token JWT**: Envía una solicitud POST a `/api/token/` con tus credenciales:

```json
{
    "email": "tu_email@email.com",
    "password": "tu_contraseña"
}
```

2. **Usar el token en solicitudes**: Incluye el token en el encabezado de tus solicitudes:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

3. **Refrescar el token**: Cuando el token expire, puedes obtener uno nuevo enviando el token de refresco a `/api/token/refresh/`:

```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

## 📚 Endpoints de la API

### Documentación interactiva
- **Swagger UI**: `/swagger/` - Interfaz interactiva para probar la API
- **ReDoc**: `/redoc/` - Documentación detallada en formato legible

### Autenticación
- **Obtener token**: `POST /api/token/` - Generar un token JWT válido
- **Refrescar token**: `POST /api/token/refresh/` - Renovar un token expirado

### Usuarios
- **Registrar nuevo usuario**: `POST /api/register/` - Crear una nueva cuenta de usuario
- **Obtener perfil de usuario**: `GET /api/user/` - Ver información del perfil actual
- **Actualizar perfil de usuario**: `PUT /api/user/` - Modificar datos personales
- **Obtener perfil (ruta alternativa)**: `GET /api/users/me/` - Endpoint adicional para perfil

### Tareas
- **Listar tareas**: `GET /api/tasks/` - Obtener todas las tareas del usuario
  - Parámetros de filtrado: `?search=texto` (buscar en título/descripción)
  - Parámetros de ordenación: `?ordering=created_at` o `?ordering=-created_at` (descendente)
  - Filtrar por estado: `?status=pending` | `in_progress` | `completed`
  - Filtrar por prioridad: `?priority=low` | `medium` | `high`
- **Crear tarea**: `POST /api/tasks/` - Añadir una nueva tarea
- **Obtener tarea**: `GET /api/tasks/{id}/` - Ver detalles de una tarea específica
- **Actualizar tarea**: `PUT /api/tasks/{id}/` - Modificar una tarea existente
- **Actualización parcial**: `PATCH /api/tasks/{id}/` - Actualizar solo algunos campos
- **Eliminar tarea**: `DELETE /api/tasks/{id}/` - Borrar una tarea

### Ejemplos de uso con Postman

#### Obtener token de autenticación:
- Método: `POST`
- URL: `http://localhost:8000/api/token/`
- Body (raw JSON):
```json
{
    "email": "usuario@ejemplo.com",
    "password": "contraseña_segura"
}
```
- Respuesta:
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Registrar un nuevo usuario:
- Método: `POST`
- URL: `http://localhost:8000/api/register/`
- Body (raw JSON):
```json
{
    "username": "nuevo_usuario",
    "email": "usuario@ejemplo.com",
    "password": "contraseña_segura",
    "password2": "contraseña_segura",
    "first_name": "Nombre",
    "last_name": "Apellido"
}
```
- Respuesta:
```json
{
    "status": "success",
    "message": "Usuario registrado correctamente. Ya puede iniciar sesión.",
    "data": {
        "id": 1,
        "username": "nuevo_usuario",
        "email": "usuario@ejemplo.com"
    }
}
```

#### Obtener perfil de usuario:
- Método: `GET`
- URL: `http://localhost:8000/api/user/` o `http://localhost:8000/api/users/me/`
- Headers: `Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- Respuesta:
```json
{
    "status": "success",
    "message": "Perfil de usuario recuperado correctamente",
    "data": {
        "id": 1,
        "email": "usuario@ejemplo.com",
        "username": "nuevo_usuario",
        "first_name": "Nombre",
        "last_name": "Apellido",
        "last_login": "2023-05-21T14:30:15.123456Z",
        "date_joined": "2023-05-15T10:20:30.123456Z",
        "task_count": 5
    }
}
```

#### Crear una tarea:
- Método: `POST`
- URL: `http://localhost:8000/api/tasks/`
- Headers: `Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- Body (raw JSON):
```json
{
    "title": "Implementar autenticación",
    "description": "Configurar JWT y permisos de usuario",
    "status": "in_progress",
    "priority": "high",
    "due_date": "2025-06-15T12:00:00Z"
}
```
- Respuesta:
```json
{
    "id": 1,
    "title": "Implementar autenticación",
    "description": "Configurar JWT y permisos de usuario",
    "status": "in_progress",
    "status_display": "En proceso",
    "priority": "high",
    "priority_display": "Alta",
    "created_at": "2025-05-21T15:30:45.123456Z",
    "due_date": "2025-06-15T12:00:00Z",
    "is_overdue": false,
    "days_remaining": 22,
    "user": 1,
    "username": "nuevo_usuario"
}
```

#### Listar tareas con filtros:
- Método: `GET`
- URL: `http://localhost:8000/api/tasks/?status=pending&priority=high&ordering=-created_at`
- Headers: `Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- Filtros disponibles:
  - `status`: Filtrar por estado (`pending`, `in_progress`, `completed`)
  - `priority`: Filtrar por prioridad (`low`, `medium`, `high`)
  - `has_due_date`: Filtrar tareas con fecha límite (`true` o `false`)
  - `is_overdue`: Filtrar tareas vencidas (`true` o `false`)
  - `due_date_before`: Filtrar tareas con fecha límite anterior a una fecha (`YYYY-MM-DD`)
  - `due_date_after`: Filtrar tareas con fecha límite posterior a una fecha (`YYYY-MM-DD`)
- Opciones de ordenamiento:
  - `ordering=due_date`: Ordenar por fecha límite ascendente
  - `ordering=-due_date`: Ordenar por fecha límite descendente
  - `ordering=created_at`: Ordenar por fecha de creación ascendente
  - `ordering=-created_at`: Ordenar por fecha de creación descendente
  - `ordering=priority`: Ordenar por prioridad ascendente
  - `ordering=-priority`: Ordenar por prioridad descendente
- Respuesta:
```json
{
    "count": 10,
    "next": "http://localhost:8000/api/tasks/?page=2&status=pending&priority=high",
    "previous": null,
    "results": [
        {
            "id": 5,
            "title": "Planificar sprint",
            "description": "Definir tareas para el próximo sprint",
            "status": "pending",
            "status_display": "Pendiente",
            "priority": "high",
            "priority_display": "Alta",
            "created_at": "2025-05-20T09:15:30.123456Z",
            "due_date": "2025-06-10T18:00:00Z",
            "is_overdue": false,
            "days_remaining": 17,
            "user": 1,
            "username": "nuevo_usuario"
        },
        ...
    ],
    "meta": {
        "total_count": 15,
        "status_counts": {
            "pending_count": 10,
            "in_progress_count": 3,
            "completed_count": 2
        },
        "priority_counts": {
            "low_count": 4,
            "medium_count": 6,
            "high_count": 5
        },
        "overdue_count": 2,
        "tasks_with_due_date": 12
    }
}
```

---

## 🛠️ Comandos útiles

### Gestión de contenedores Docker:
```bash
# Ver logs en tiempo real
docker-compose logs -f

# Reiniciar contenedores
docker-compose restart

# Detener contenedores
docker-compose down

# Reconstruir imágenes y reiniciar contenedores
docker-compose up -d --build
```

### Comandos de Django:
```bash
# Acceder a la shell de Django
docker-compose exec web python manage.py shell

# Crear nuevas migraciones
docker-compose exec web python manage.py makemigrations

# Aplicar migraciones
docker-compose exec web python manage.py migrate

# Recolectar archivos estáticos
docker-compose exec web python manage.py collectstatic --noinput

# Crear superusuario
docker-compose exec web python manage.py createsuperuser
```

### Gestión de base de datos:
```bash
# Acceder a la consola de PostgreSQL
docker-compose exec db psql -U postgres -d taskapi

# Realizar backup de la base de datos
docker-compose exec db pg_dump -U postgres taskapi > backup.sql

# Restaurar backup
cat backup.sql | docker-compose exec -T db psql -U postgres -d taskapi
```

### Desarrollo local (sin Docker):
```powershell
# Activar entorno virtual
.\venv\Scripts\Activate

# Ejecutar servidor de desarrollo
python manage.py runserver

# Ejecutar pruebas
python manage.py test
```

---

## 🔧 Detalles técnicos

### Estados de tareas
El sistema implementa un flujo de trabajo de tareas con los siguientes estados:

| Estado | Valor en API | Descripción |
|--------|--------------|-------------|
| Pendiente | `pending` | Tarea creada pero no iniciada |
| En proceso | `in_progress` | Tarea en la que se está trabajando |
| Completada | `completed` | Tarea finalizada |

### Prioridades de tareas
El sistema permite asignar prioridades a las tareas para una mejor organización:

| Prioridad | Valor en API | Descripción |
|-----------|--------------|-------------|
| Baja | `low` | Tareas de baja importancia o urgencia |
| Media | `medium` | Tareas con importancia moderada (valor predeterminado) |
| Alta | `high` | Tareas críticas o urgentes que requieren atención inmediata |

### Fecha límite y campos calculados
El sistema incluye campos relacionados con la fecha límite para gestionar mejor los tiempos de las tareas:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `due_date` | DateTimeField | Fecha y hora límite para completar la tarea (opcional) |
| `is_overdue` | Boolean | Indica si la tarea está vencida (true si la fecha actual es posterior a la fecha límite y la tarea no está completada) |
| `days_remaining` | Integer | Número de días restantes hasta la fecha límite (0 si la fecha ya ha pasado, null si no hay fecha límite) |

**Notas importantes:**
- La fecha límite debe ser una fecha futura al crear o actualizar una tarea
- Una tarea se considera vencida solo si no está completada y la fecha límite ha pasado
- Los campos `is_overdue` y `days_remaining` son campos calculados y de solo lectura

### Estructura de autenticación
La implementación JWT utiliza las siguientes características:

- Tokens de acceso con duración de 15 minutos
- Tokens de refresco con duración de 24 horas
- Autenticación mediante encabezado `Authorization: Bearer <token>`
- Control de acceso basado en propietario de recursos

### Seguridad implementada
- Validación de contraseñas robusta
- Protección contra CSRF
- Configuración de CORS para entornos de producción
- Sanitización de entradas de usuario
- Validación de datos en serializadores

---

## ❓ Solución de problemas frecuentes

### Error de conexión a la base de datos
Si encuentras errores como `could not translate host name "db" to address: Host desconocido`:

1. Verifica que los contenedores Docker estén ejecutándose: `docker-compose ps`
2. Asegúrate de que las variables de entorno están configuradas correctamente en `.env`
3. Intenta reiniciar los contenedores: `docker-compose restart`

### Errores de migración
Si encuentras errores al aplicar migraciones:

1. Intenta reiniciar desde cero: 
   ```bash
   docker-compose down
   docker volume prune  # ¡Cuidado! Esto eliminará todos los datos
   docker-compose up -d
   docker-compose exec web python manage.py migrate
   ```

2. Si aparece `InconsistentMigrationHistory`, puede que necesites recrear la base de datos:
   ```bash
   docker-compose exec db psql -U postgres
   # En la consola de PostgreSQL:
   DROP DATABASE taskapi;
   CREATE DATABASE taskapi;
   # Luego vuelve a aplicar las migraciones
   ```

### Problemas de autenticación
Si los tokens no funcionan:

1. Verifica que estás incluyendo el token completo en el encabezado `Authorization: Bearer <token>`
2. Comprueba que el token no ha expirado
3. Asegúrate de que estás usando el token de acceso, no el de refresco
4. Solicita un nuevo token con el endpoint de refresco

---

## 📊 Características detalladas

### Sistema de Tareas
- **Estados de tareas**: Las tareas pueden tener tres estados: "pendiente", "en proceso" y "completada"
- **Prioridades**: Las tareas pueden tener tres niveles de prioridad: "baja", "media" y "alta"
- **Filtrado y búsqueda**: Filtra tareas por título, descripción, estado y prioridad
- **Ordenamiento**: Ordena tareas por fecha, título, estado o prioridad
- **Estadísticas**: La API proporciona estadísticas sobre tareas por estado y prioridad

### Gestión de usuarios
- **Registro seguro**: Validación robusta de contraseñas y datos de usuario
- **Perfil de usuario**: Vista y actualización de información personal
- **Rutas alternativas**: Acceso al perfil a través de dos endpoints diferentes

### Seguridad
- **Autenticación JWT**: Tokens de acceso y refresco
- **Permisos granulares**: Cada usuario solo puede ver y modificar sus propias tareas
- **Validación de entradas**: Validación robusta de todos los datos enviados a la API
- **CORS configurado**: Permite integrarse con aplicaciones frontend

---

## 🌟 Casos de uso comunes

### Flujo de trabajo de tareas
1. **Crear una tarea**: Inicialmente con estado "pendiente"
2. **Actualizar a "en proceso"**: Cuando se comienza a trabajar en la tarea
3. **Marcar como "completada"**: Cuando la tarea se finaliza
4. **Monitorear progreso**: Visualizar estadísticas de tareas por estado

### Gestión de usuarios
1. **Registro de usuario**: Crear una cuenta nueva
2. **Autenticación**: Obtener token JWT
3. **Ver perfil**: Consultar datos personales
4. **Actualizar perfil**: Modificar nombre, apellido y otros datos

---

## 🧪 Pruebas

Para ejecutar todas las pruebas:

```bash
docker-compose exec web python manage.py test
```

Para pruebas específicas:

```bash
# Probar solo la app de tareas
docker-compose exec web python manage.py test tasks

# Probar solo la app de usuarios
docker-compose exec web python manage.py test users
```

---

## 🤝 Contribución

1. Haz un fork del proyecto
2. Crea una rama para tu funcionalidad (`git checkout -b feature/amazing-feature`)
3. Haz commit de tus cambios (`git commit -m 'Add some amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

### Guía de estilo y convenciones
- Seguimos PEP 8 para el estilo de código Python
- Utilizamos docstrings en formato Google Style para documentación
- Todas las nuevas características deben incluir pruebas unitarias
- Los mensajes de commit deben ser claros y descriptivos

---

## 📋 Roadmap

Características planeadas para futuras versiones:

- [x] Prioridades para tareas (baja, media, alta)
- [ ] Categorías para tareas
- [ ] Tareas recurrentes
- [ ] Notificaciones por correo electrónico
- [ ] Integración con calendarios externos
- [ ] Cliente web con React.js
- [ ] Aplicación móvil con React Native

---

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
