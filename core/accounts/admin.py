from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "is_superuser", "last_login")
    list_filter = ("username", "is_superuser")
    search_fields = ("username",)
    
    fieldsets = (
        ("Authentication", {
            'fields': (
                'username', 'password', 
            ),
        }),
        ("Permissions", {
            'fields': (
                'is_staff', 'is_active', 'is_superuser'
            ),
        }),
        ("Groupe permissions", {
            'fields': (
                'groups', 'user_permissions'
            ),
        }),
        ("Important date", {
            'fields': (
                'last_login',
            ),
        }),
    )
    
    add_fieldsets = (
        ("Authentication", {
            "classes" : ("wide", ),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )