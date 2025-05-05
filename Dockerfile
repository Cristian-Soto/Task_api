FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=config.settings


EXPOSE 8000

WORKDIR /app

COPY backend/ /app/

RUN pip install --upgrade pip
RUN pip install django djangorestframework psycopg2-binary python-decouple drf-yasg djangorestframework-simplejwt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]