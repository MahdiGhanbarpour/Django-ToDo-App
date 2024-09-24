from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from django.core.cache import cache
from django.urls import reverse_lazy
import requests


# Create your views here.
class TodoListView(LoginRequiredMixin, ListView):
    """
    A view for showing list of tasks and weather data
    """

    model = Task
    context_object_name = "tasks"
    template_name = "todo/index.html"

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)

    def get_weather_data(self):
        weather_data = cache.get("weather_data")

        if not weather_data:
            response = requests.get(
                "http://api.weatherapi.com/v1/current.json?"
                "key=778b31e7497747888dc100540230907&q=Bushehr&aqi=no"
            )

            if response.status_code == 200:
                weather_data = response.json()
                weather_data["source"] = "API"
                cache.set("weather_data", weather_data, 1200)
        else:
            weather_data["source"] = "Cache"

        return weather_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["weather_data"] = self.get_weather_data()
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    """
    A view for creating new tasks
    """

    model = Task
    fields = ["title"]
    success_url = reverse_lazy("todo:task-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """
    A view for deleting tasks
    """

    model = Task
    success_url = reverse_lazy("todo:task-list")

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)


class TaskToggleView(LoginRequiredMixin, UpdateView):
    """
    A view for changing is_done property of selected task
    """

    model = Task
    fields = []
    success_url = reverse_lazy("todo:task-list")

    def form_valid(self, form):
        form.instance.is_done = not form.instance.is_done
        form.save()
        return super().form_valid(form)

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """
    A view for changing title of selected task
    """

    model = Task
    fields = ["title"]
    template_name = "todo/update_task.html"
    success_url = reverse_lazy("todo:task-list")

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)
