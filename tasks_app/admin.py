"""Admin configuration for tasks and comments."""

from django.contrib import admin

from .models import Comment, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Show the key task fields and allow filtering in the admin list."""

    list_display = ("id", "title", "board", "status", "priority")
    list_filter = ("status", "priority")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Show comments with their task and author in the admin list."""

    list_display = ("id", "task", "author", "created_at")
