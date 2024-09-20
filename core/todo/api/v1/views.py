from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import TaskSerializer
from ...models import Task
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import action


class TaskModelViewSet(viewsets.ModelViewSet):
    """A ModelViewSet for tasks"""

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = TaskSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_done"]
    search_fields = ["title"]
    ordering_fields = ["created_date"]

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)

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
