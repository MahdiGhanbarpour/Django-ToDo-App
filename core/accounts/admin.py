from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PasswordReset

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "is_superuser", 'is_verified', "last_login")
    list_filter = ("username", "email", "is_superuser", 'is_verified')
    search_fields = ("username",)
    
    fieldsets = (
        ("Authentication", {
            'fields': (
                'username', "email", 'password', 
            ),
        }),
        ("Permissions", {
            'fields': (
                'is_staff', 'is_active', 'is_superuser', 'is_verified'
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
            'fields': ('username', "email", 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser', 'is_verified'),
        }),
    )
    
admin.site.register(PasswordReset)