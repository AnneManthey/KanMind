"""Views for boards."""

from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from boards_app.models import Board

from .serializers import BoardSerializer


class BoardListCreateView(generics.ListCreateAPIView):
    """List the user's boards and create a new board."""

    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return boards the user owns or is a member of."""
        user = self.request.user
        return Board.objects.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()

    def perform_create(self, serializer):
        """Set the requesting user as owner of the new board."""
        serializer.save(owner=self.request.user)