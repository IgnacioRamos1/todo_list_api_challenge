from django.urls import path
from . import views


urlpatterns = [
    path('tasks/', views.task_list_view, name='task-list'),
]
