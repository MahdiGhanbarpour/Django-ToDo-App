from django.urls import path
from . import views

app_name = "todo"

urlpatterns = [
    path('', views.TodoListView.as_view(), name="task-list"),
    path('task/create/', views.TaskCreateView.as_view(), name="task-create"),
]