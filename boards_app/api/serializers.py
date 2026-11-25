"""Serializers for boards."""

from rest_framework import serializers

from auth_app.api.serializers import UserSummarySerializer
from boards_app.models import Board
from tasks_app.api.serializers import BoardTaskSerializer
from tasks_app.models import Task


class BoardSerializer(serializers.ModelSerializer):
    """Serialize a board with its counters for the list and create."""

    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = (
            "id",
            "title",
            "member_count",
            "ticket_count",
            "tasks_to_do_count",
            "tasks_high_prio_count",
            "owner_id",
            "members",
        )
        # members is input only; the response shows member_count instead.
        extra_kwargs = {"members": {"write_only": True}}

    def get_member_count(self, board):
        """Return the number of members listed on the board."""
        # The owner is only counted if listed in members.
        return board.members.count()

    def get_ticket_count(self, board):
        """Return the number of tasks on the board."""
        return board.tasks.count()

    def get_tasks_to_do_count(self, board):
        """Return the number of tasks in the to-do status."""
        return board.tasks.filter(status=Task.Status.TO_DO).count()

    def get_tasks_high_prio_count(self, board):
        """Return the number of tasks with high priority."""
        return board.tasks.filter(priority=Task.Priority.HIGH).count()


class BoardDetailSerializer(serializers.ModelSerializer):
    """Show one board with its members and tasks (GET detail)."""

    members = UserSummarySerializer(many=True, read_only=True)
    tasks = BoardTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ("id", "title", "owner_id", "members", "tasks")


class BoardUpdateSerializer(serializers.ModelSerializer):
    """Update title and members of a board (PATCH)."""

    owner_data = UserSummarySerializer(source="owner", read_only=True)
    members_data = UserSummarySerializer(
        source="members", many=True, read_only=True
    )

    class Meta:
        model = Board
        fields = ("id", "title", "owner_data", "members", "members_data")
        # members is input only; the response shows members_data instead.
        extra_kwargs = {"members": {"write_only": True}}


class EmailCheckSerializer(serializers.Serializer):
    """Validate the email query parameter of the email check."""

    email = serializers.EmailField()