FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY backend/ /app/

RUN pip install --upgrade pip
RUN pip install django djangorestframework psycopg2-binary python-decouple drf-yasg djangorestframework-simplejwt
