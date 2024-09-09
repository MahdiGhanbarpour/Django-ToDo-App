from django.urls import path
from . import views

app_name = "todo"

urlpatterns = [
    path('', views.TodoListView.as_view(), name="task-list"),
    path('task/create/', views.TaskCreateView.as_view(), name="task-create"),
    path('task/delete/<int:pk>', views.TaskDeleteView.as_view(), name="task-delete"),
    path('task/toggle/<int:pk>', views.TaskToggleView.as_view(), name="task-toggle"),
    path('task/update/<int:pk>', views.TaskUpdateView.as_view(), name="task-update"),
]