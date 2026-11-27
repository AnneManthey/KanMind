"""Custom permissions for tasks."""

from rest_framework.permissions import BasePermission

from boards_app.api.permissions import is_board_member


class IsTaskBoardMember(BasePermission):
    """Allow access only to members or the owner of the task's board."""

    def has_object_permission(self, request, view, obj):
        """Return True if the user belongs to the board of the task."""
        return is_board_member(request.user, obj.board)


class IsTaskCreatorOrBoardOwner(BasePermission):
    """Allow access only to the task creator or the board owner."""

    def has_object_permission(self, request, view, obj):
        """Return True if the user created the task or owns its board."""
        user = request.user
        return obj.created_by == user or obj.board.owner == user


class IsCommentAuthor(BasePermission):
    """Allow access only to the author of the comment."""

    def has_object_permission(self, request, view, obj):
        """Return True if the user wrote the comment."""
        return obj.author == request.user
