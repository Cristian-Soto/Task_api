from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from backend.tasks.models import Task
from backend.tasks.serializers import TaskSerializer

# Create your views here.

def hello_world(request):
    return JsonResponse({"message": "Hola, mundo"})

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
