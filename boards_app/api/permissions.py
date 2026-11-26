"""Custom permissions for boards."""

from rest_framework.permissions import BasePermission


def is_board_member(user, board) -> bool:
    """Return True if the user owns the board or is one of its members.

    Args:
        user: The user to check.
        board: The board the user wants to access.

    Returns:
        True if the user is the owner or listed in ``members``.
    """
    return (
        board.owner == user
        or board.members.filter(pk=user.pk).exists()
    )


class IsBoardOwnerOrMember(BasePermission):
    """Allow access only to the owner or a member of the board."""

    def has_object_permission(self, request, view, obj):
        """Return True if the user owns the board or is a member."""
        return is_board_member(request.user, obj)


class IsBoardOwner(BasePermission):
    """Allow access only to the owner of the board."""

    def has_object_permission(self, request, view, obj):
        """Return True if the user owns the board."""
        return obj.owner == request.user
