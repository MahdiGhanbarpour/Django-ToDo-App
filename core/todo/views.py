from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .models import Task
from django.urls import reverse_lazy

# Create your views here.
class TodoListView(ListView):
    '''
    A view for showing list of tasks
    '''
    model = Task
    context_object_name = "tasks"
    template_name = "todo/index.html"
    
class TaskCreateView(CreateView):
    '''
    A view for creating new tasks
    '''
    model = Task
    fields = ["title"]
    success_url = reverse_lazy("todo:task-list")
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class TaskDeleteView(DeleteView):
    '''
    A view for deleting tasks
    '''
    model = Task
    success_url = reverse_lazy("todo:task-list")
    
class TaskToggleView(UpdateView):
    '''
    A view for changing is_done property of selected task
    '''
    model = Task
    fields = []
    success_url = reverse_lazy("todo:task-list")
    
    def form_valid(self, form) :
        form.instance.is_done = not form.instance.is_done
        form.save()
        return super().form_valid(form)
    
class TaskUpdateView(UpdateView):
    '''
    A view for changing title of selected task
    '''
    model = Task
    fields = ["title"]
    template_name = "todo/update_task.html"
    success_url = reverse_lazy("todo:task-list")