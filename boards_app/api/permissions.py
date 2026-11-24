"""Custom permissions for boards."""

from rest_framework.permissions import BasePermission


class IsBoardOwnerOrMember(BasePermission):
    """Allow access only to the owner or a member of the board."""

    def has_object_permission(self, request, view, obj):
        """Return True if the user owns the board or is a member."""
        user = request.user
        return obj.owner == user or obj.members.filter(pk=user.pk).exists()


class IsBoardOwner(BasePermission):
    """Allow access only to the owner of the board."""

    def has_object_permission(self, request, view, obj):
        """Return True if the user owns the board."""
        return obj.owner == request.user