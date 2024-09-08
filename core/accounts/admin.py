from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "is_superuser", "last_login")
    list_filter = ("username", "is_superuser")
    search_fields = ("username",)