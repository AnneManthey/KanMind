"""Serializers for tasks."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from auth_app.api.serializers import UserSummarySerializer
from boards_app.api.permissions import is_board_member
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

    def validate(self, attrs):
        """Ensure assignee and reviewer are members of the task's board.

        Args:
            attrs: The field values that passed the field validation.

        Returns:
            The unchanged attrs if all users belong to the board.

        Raises:
            ValidationError: If assignee or reviewer is not a member.
        """
        board = attrs.get("board", getattr(self.instance, "board", None))
        for field in ("assignee", "reviewer"):
            user = attrs.get(field)
            if user is not None and not is_board_member(user, board):
                raise serializers.ValidationError(
                    {f"{field}_id": "User must be a member of the board."}
                )
        return attrs


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