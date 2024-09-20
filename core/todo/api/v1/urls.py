from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("todo", views.TaskModelViewSet, basename="todo")

app_name = "api-v1"

urlpatterns = router.urls
