"""Views for tasks."""

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from boards_app.api.permissions import is_board_member
from boards_app.models import Board
from tasks_app.models import Task

from .permissions import IsTaskBoardMember, IsTaskCreatorOrBoardOwner
from .serializers import TaskSerializer, TaskUpdateSerializer


class TaskCreateView(generics.CreateAPIView):
    """Create a task on a board the user belongs to."""

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Check board access before the usual create flow."""
        self.check_board_access(request.data.get("board"))
        return super().create(request, *args, **kwargs)

    def check_board_access(self, board_id):
        """Raise 404 for an unknown board and 403 for non-members.

        Args:
            board_id: The board id from the request body.

        Raises:
            Http404: If no board with this id exists.
            PermissionDenied: If the user is not a member of the board.
        """
        if not str(board_id).isdigit():
            return
        board = get_object_or_404(Board, pk=board_id)
        if not is_board_member(self.request.user, board):
            raise PermissionDenied("You must be a member of this board.")

    def perform_create(self, serializer):
        """Store the requesting user as creator of the task."""
        serializer.save(created_by=self.request.user)


class TaskDetailView(generics.UpdateAPIView, generics.DestroyAPIView):
    """Update or delete a single task."""

    queryset = Task.objects.all()
    serializer_class = TaskUpdateSerializer
    http_method_names = ["patch", "delete", "options"]

    def get_permissions(self):
        """Allow creator or board owner to delete, members to update."""
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsTaskCreatorOrBoardOwner()]
        return [IsAuthenticated(), IsTaskBoardMember()]


class AssignedToMeView(generics.ListAPIView):
    """List all tasks assigned to the requesting user."""

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return tasks where the user is the assignee."""
        return Task.objects.filter(assignee=self.request.user)


class ReviewingView(generics.ListAPIView):
    """List all tasks the requesting user has to review."""

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return tasks where the user is the reviewer."""
        return Task.objects.filter(reviewer=self.request.user)