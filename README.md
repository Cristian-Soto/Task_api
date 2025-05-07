# 🐍 Django REST API con PostgreSQL en Docker

Este proyecto es una API RESTful construida con Django, Django REST Framework y PostgreSQL, todo en contenedores Docker. Proporciona un sistema de gestión de tareas con autenticación JWT.

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

### 2. Iniciar los contenedores Docker

```bash
docker-compose up -d
```

Este comando construirá las imágenes necesarias e iniciará los contenedores de Django y PostgreSQL. La API estará disponible en `http://localhost:8000`.

### 3. Crear un superusuario (opcional)

```bash
docker-compose exec web python manage.py createsuperuser
```

Sigue las instrucciones para crear un superusuario que te permitirá acceder al panel de administración.

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
- **Swagger UI**: `/swagger/`
- **ReDoc**: `/redoc/`

### Autenticación
- **Obtener token**: `POST /api/token/`
- **Refrescar token**: `POST /api/token/refresh/`

### Tareas
- **Listar/Crear tareas**: `GET/POST /api/tasks/`
- **Obtener/Actualizar/Eliminar tarea**: `GET/PUT/DELETE /api/tasks/{id}/`

### Ejemplos de uso con Postman

#### Crear una tarea:
- Método: `POST`
- URL: `http://localhost:8000/api/tasks/`
- Headers: `Authorization: Bearer tu_token`
- Body:
```json
{
    "title": "Mi nueva tarea",
    "description": "Detalles de la tarea",
    "completed": false
}
```

#### Listar tareas:
- Método: `GET`
- URL: `http://localhost:8000/api/tasks/`
- Headers: `Authorization: Bearer tu_token`

---

## 🛠️ Comandos útiles

### Ver logs de los contenedores:
```bash
docker-compose logs
```

### Acceder a la shell de Django:
```bash
docker-compose exec web python manage.py shell
```

### Ejecutar migraciones:
```bash
docker-compose exec web python manage.py migrate
```

### Detener los contenedores:
```bash
docker-compose down
```

---

## 📝 Estructura del proyecto

```
task_api/
├── backend/             # Código principal de Django
│   ├── config/          # Configuración del proyecto
│   ├── tasks/           # App para gestión de tareas
│   └── users/           # App para gestión de usuarios
├── docker-compose.yml   # Configuración de Docker Compose
├── Dockerfile           # Instrucciones para construir la imagen Docker
├── manage.py            # Script de gestión de Django
└── requirements.txt     # Dependencias del proyecto
```

---

## 🤝 Contribución

1. Haz un fork del proyecto
2. Crea una rama para tu funcionalidad (`git checkout -b feature/amazing-feature`)
3. Haz commit de tus cambios (`git commit -m 'Add some amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
