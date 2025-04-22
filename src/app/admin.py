from django.contrib import admin

# Register your models here.
from .models import (
    User,
    ListToDo,
)


class Users(admin.ModelAdmin):
    list_display = ("id", "user", "email", "password", "deleted")
    list_filter = ("id", "user", "email")
    list_display_links = ("id", "user", "email")
    search_fields = ("user",)
    list_per_page = 20


admin.site.register(User, Users)


class ListToDos(admin.ModelAdmin):
    list_display = (
        "id",
        "task",
        "is_complete",
        "user",
        "finish_date",
        "created_at",
        "deleted",
    )
    list_filter = ("id", "task")
    list_display_links = ("id", "user", "task")
    search_fields = ("task",)
    list_per_page = 20


admin.site.register(ListToDo, ListToDos)
