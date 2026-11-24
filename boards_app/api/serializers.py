"""Serializers for boards."""

from rest_framework import serializers

from boards_app.models import Board
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
        # The owner is only counted if listed in members (per academy).
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