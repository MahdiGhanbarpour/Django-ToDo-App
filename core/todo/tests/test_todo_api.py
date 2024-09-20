import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from ..models import Task


@pytest.fixture
def common_user():
    user = User.objects.create_user("Test", "Test@test.com", "Test1234")
    return user


@pytest.fixture
def common_task(common_user):
    task = Task.objects.create(author=common_user, title="Test")
    return task


@pytest.mark.django_db
class TestPostApi:
    client = APIClient()

    def test_get_todo_list_response_200_status(self):
        url = reverse("todo:api-v1:todo-list")
        response = self.client.get(url)

        assert response.status_code == 200

    def test_post_create_task_anonymous_response_401_status(self):
        url = reverse("todo:api-v1:todo-list")
        response = self.client.post(url)

        assert response.status_code == 401

    def test_post_create_task_logged_in_response_201_status(self, common_user):
        self.client.force_login(common_user)
        url = reverse("todo:api-v1:todo-list")

        data = {"title": "Test"}
        response = self.client.post(url, data)

        assert response.status_code == 201
        assert Task.objects.filter(pk=response.json()["id"]).exists()

    def test_post_create_task_invalid_data_response_400_status(self, common_user):
        self.client.force_login(common_user)
        url = reverse("todo:api-v1:todo-list")

        data = {}
        response = self.client.post(url, data)

        assert response.status_code == 400

    def test_get_task_detail_response_200_status(self, common_task):
        url = reverse("todo:api-v1:todo-detail", kwargs={"pk": common_task.id})
        response = self.client.get(url)

        assert response.status_code == 200

    def test_get_incorrect_task_detail_response_404_status(self):
        url = reverse("todo:api-v1:todo-detail", kwargs={"pk": 8155161})
        response = self.client.get(url)

        assert response.status_code == 404

    def test_put_task_detail_anonymous_response_401_status(self, common_task):
        data = {"title": "Edited Test", "is_done": True}
        url = reverse("todo:api-v1:todo-detail", kwargs={"pk": common_task.id})

        response = self.client.put(url, data)

        assert response.status_code == 401

    def test_put_task_detail_logged_in_response_200_status(
        self, common_user, common_task
    ):
        self.client.force_login(common_user)

        data = {"title": "Edited Test", "is_done": True}
        url = reverse("todo:api-v1:todo-detail", kwargs={"pk": common_task.id})

        response = self.client.put(url, data)

        assert response.status_code == 200

    def test_delete_task_detail_anonymous_response_401_status(self, common_task):
        url = reverse("todo:api-v1:todo-detail", kwargs={"pk": common_task.id})

        response = self.client.delete(url)

        assert response.status_code == 401

    def test_delete_task_detail_logged_in_response_204_status(
        self, common_user, common_task
    ):
        self.client.force_login(common_user)
        common_task_id = common_task.id

        url = reverse("todo:api-v1:todo-detail", kwargs={"pk": common_task.id})

        response = self.client.delete(url)

        assert response.status_code == 204
        assert not Task.objects.filter(pk=common_task_id).exists()

    def test_post_task_detail_change_status_anonymous_response_401_status(
        self, common_task
    ):
        url = reverse("todo:api-v1:todo-toggle-status", kwargs={"pk": common_task.id})

        response = self.client.post(url)

        assert response.status_code == 401

    def test_post_task_detail_change_status_logged_in_response_200_status(
        self, common_user, common_task
    ):
        self.client.force_login(common_user)
        common_task_id = common_task.id

        url = reverse("todo:api-v1:todo-toggle-status", kwargs={"pk": common_task.id})

        response = self.client.post(url)

        assert response.status_code == 200
        assert Task.objects.get(pk=common_task_id).is_done
