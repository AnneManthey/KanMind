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


class TaskUpdateSerializer(TaskSerializer):
    """Update a task; the board cannot be changed."""

    comments_count = None

    class Meta(TaskSerializer.Meta):
        fields = (
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "assignee_id",
            "reviewer_id",
            "due_date",
        )

    def validate(self, attrs):
        """Reject a changed board, then run the membership checks.

        Args:
            attrs: The field values that passed the field validation.

        Returns:
            The validated attrs.

        Raises:
            ValidationError: If the request contains a board.
        """
        if "board" in self.initial_data:
            raise serializers.ValidationError(
                {"board": "Changing the board is not allowed."}
            )
        return super().validate(attrs)