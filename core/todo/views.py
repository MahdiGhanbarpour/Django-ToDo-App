from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import Task
from django.urls import reverse_lazy

# Create your views here.
class TodoListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "index.html"
    
class TaskCreateView(CreateView):
    model=Task
    fields = ["title"]
    success_url = reverse_lazy("todo:task-list")
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)