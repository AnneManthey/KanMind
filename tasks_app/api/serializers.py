"""Serializers for tasks."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from auth_app.api.serializers import UserSummarySerializer
from tasks_app.models import Task

User = get_user_model()


class BoardTaskSerializer(serializers.ModelSerializer):
    """Show a task as nested part of a board (read only)."""

    assignee = UserSummarySerializer(read_only=True)
    reviewer = UserSummarySerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "due_date",
            "comments_count",
        )

    def get_comments_count(self, task):
        """Return the number of comments on the task."""
        return task.comments.count()


class TaskSerializer(serializers.ModelSerializer):
    """Create tasks and show them in the task lists."""

    assignee = UserSummarySerializer(read_only=True)
    reviewer = UserSummarySerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="assignee",
        write_only=True,
        required=False,
        allow_null=True,
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="reviewer",
        write_only=True,
        required=False,
        allow_null=True,
    )
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            "id",
            "board",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "assignee_id",
            "reviewer_id",
            "due_date",
            "comments_count",
        )

    def get_comments_count(self, task):
        """Return the number of comments on the task."""
        return task.comments.count()