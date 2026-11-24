"""Admin configuration for boards."""

from django.contrib import admin

from .models import Board


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """Show boards with their owner in the admin list."""

    list_display = ("id", "title", "owner")
    filter_horizontal = ("members",)
