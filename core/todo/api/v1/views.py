from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerializer
from ...models import Task
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.core.cache import cache
import requests


class TaskModelViewSet(viewsets.ModelViewSet):
    """A ModelViewSet for tasks"""

    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_done"]
    search_fields = ["title"]
    ordering_fields = ["created_date"]

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)

    @action(detail=False, methods=["GET"], url_path="weather-status")
    def get_weather_status(self, request):
        """A action to get weather status"""
        weather_data = cache.get("weather_data_api")

        if not weather_data:
            response = requests.get(
                "http://api.weatherapi.com/v1/current.json"
                "?key=778b31e7497747888dc100540230907&q=Bushehr&aqi=no"
            )

            if response.status_code == 200:
                weather_data = response.json()
                weather_data["source"] = "API"
                cache.set("weather_data_api", weather_data, 1200)
            else:
                return Response({"detail": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            weather_data["source"] = "Cache"

        return Response(weather_data, status=status.HTTP_200_OK)

    @action(methods=["GET", "POST"], detail=True, url_path="change-status")
    def toggle_status(self, request, pk):
        """A extra action to toggle tasks status"""
        task = self.get_object()

        if task.author != request.user:
            return Response(
                {"detail": "You are not allowed to change the status of this task."},
                status=403,
            )

        task.is_done = not task.is_done
        task.save()

        return Response({"detail": f"Task status changed to {task.is_done}"})
