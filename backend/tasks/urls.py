from django.urls import path
from .views import TaskListCreateView, TaskRetrieveUpdateDestroyView, hello_world

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list-create'),
    path('<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),
    path('hello/', hello_world, name='hello_world'),
]