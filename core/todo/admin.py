from django.contrib import admin
from .models import Task

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_done")
    list_filter = ("is_done", )
    search_fields = ("title", "author")
    
    fieldsets = (
        ("", {
            'fields': ('author', 'title', 'is_done'),
        }),
    )
    
    add_fieldsets = (
        ("", {
            'fields': ('author', 'title', 'is_done'),
        }),
    )