import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from ..models import User

@pytest.fixture
def common_user():
    user = User.objects.create_user("Mahdi", "Mahdi@test.com", "Mahdi123")
    return user

@pytest.mark.django_db
class TestPostApi:
    client = APIClient()
    
    def test_post_registration_invalid_data_response_400_status(self):
        data = {"username": "Test","password": "Test1234"}
        url = reverse("accounts:api-v1:registration")
        
        response = self.client.post(url, data)
        
        assert response.status_code == 400
        
    def test_post_registration_response_201_status(self):
        data = {
            "username": "Mahdi",
            "email": "Mahdi@test.com",
            "password": "Mahdi123",
            "password1": "Mahdi123"
        }
        url = reverse("accounts:api-v1:registration")
        
        response = self.client.post(url, data)
        
        assert response.status_code == 201
        assert User.objects.filter(username=response.json()["username"]).exists()
        
    def test_get_activation_confirm_invalid_token_response_400_status(self):
        invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2NTgxNzQ0LCJpYXQiOjE3MjY1ODE0NDQsImp0aSI6IjJjYWVkNjI1ODE5MzQ2ZWNiZmViZmE3ZDA2YWY1YmE5IiwidXNlcl9pZCI6Nn0.es6UcS20Nv_2m06N-DArAg6e5pXQoGq_sNlL-cg_EIw"
        url = reverse("accounts:api-v1:activation", kwargs={"token":invalid_token})
        
        response = self.client.get(url)
        
        assert response.status_code == 400
        
    def test_post_activation_resend_invalid_data_response_400_status(self):
        data = {}
        url = reverse("accounts:api-v1:activation-resend")
        
        response = self.client.post(url, data)
        
        assert response.status_code == 400
        
    def test_post_activation_resend_response_200_status(self, common_user):
        data = {"username": common_user.username}
        url = reverse("accounts:api-v1:activation-resend")
        
        response = self.client.post(url, data)
        
        assert response.status_code == 200
        
    def test_put_change_password_anonymous_response_401_status(self):
        url = reverse("accounts:api-v1:change-password")
        
        response = self.client.post(url)
        
        assert response.status_code == 401
        
    def test_put_change_password_logged_in_invalid_data_response_400_status(self, common_user):
        self.client.force_login(common_user)
        
        data = {
            "old_password": "InvalidPassword",
            "new_password": "NewPassword123",
            "new_password1": "NewPassword123"
        }
        url = reverse("accounts:api-v1:change-password")
        
        response = self.client.put(url, data)
        
        assert response.status_code == 400
        
    def test_put_change_password_logged_in_response_200_status(self, common_user):
        self.client.force_login(common_user)
        
        data = {
            "old_password": "Mahdi123",
            "new_password": "NewPassword123",
            "new_password1": "NewPassword123"
        }
        url = reverse("accounts:api-v1:change-password")
        
        response = self.client.put(url, data)
        
        assert response.status_code == 200
        
    def test_post_reset_password_request_invalid_data_response_404_status(self):
        data = {"username":"Invalid Username", "email":"Invalid Email"}
        url = reverse("accounts:api-v1:reset-password")
        
        response = self.client.post(url, data)
        
        assert response.status_code == 404
        
    def test_post_reset_password_request_response_200_status(self, common_user):
        data = {"username":common_user.username, "email":common_user.email}
        url = reverse("accounts:api-v1:reset-password")
        
        response = self.client.post(url, data)
        
        assert response.status_code == 200
        
    def test_post_reset_password_confirm_invalid_token_response_400_status(self):
        url = reverse("accounts:api-v1:reset-password-confirm", kwargs={"token":"Invalid Token"})
        
        response = self.client.post(url)
        
        assert response.status_code == 400

    def test_post_login_token_invalid_data_response_400_status(self):
        data = {"username":"Invalid Username"}
        url = reverse("accounts:api-v1:token-login")
        
        response = self.client.post(url, data)
        
        assert response.status_code == 400
        
    def test_post_logout_token_anonymous_response_401_status(self):
        url = reverse("accounts:api-v1:token-logout")

        response = self.client.post(url)
        
        assert response.status_code == 401
        
    def test_post_jwt_create_invalid_data_response_400_status(self):
        data = {"username":"Invalid Username"}
        url = reverse("accounts:api-v1:jwt-create")
        
        response = self.client.post(url, data)
        
        assert response.status_code == 400
        
    def test_post_jwt_refresh_invalid_data_response_401_status(self):
        data = {}
        url = reverse("accounts:api-v1:jwt-refresh")
        
        response = self.client.post(url, data)
        
        assert response.status_code == 400
        
    def test_post_jwt_refresh_invalid_token_response_401_status(self):
        data = {"refresh":"Invalid Token"}
        url = reverse("accounts:api-v1:jwt-refresh")
        
        response = self.client.post(url, data)
        
        assert response.status_code == 401
        
    def test_post_jwt_verify_invalid_data_response_401_status(self):
        data = {}
        url = reverse("accounts:api-v1:jwt-verify")
        
        response = self.client.post(url, data)
        
        assert response.status_code == 400
        
    def test_post_jwt_verify_invalid_token_response_401_status(self):
        data = {"token":"Invalid Token"}
        url = reverse("accounts:api-v1:jwt-verify")
        
        response = self.client.post(url, data)
        
        assert response.status_code == 401