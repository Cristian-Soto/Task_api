# Imagen base
FROM python:3.12.3-alpine

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . .

# Instalar dependencias
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Establecer variable de entorno para Django
ENV DJANGO_SETTINGS_MODULE=config.settings

# Exponer el puerto
EXPOSE 8000

# Comando por defecto al iniciar el contenedor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]