"""Serializers for tasks."""

from rest_framework import serializers

from auth_app.api.serializers import UserSummarySerializer
from tasks_app.models import Task


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
