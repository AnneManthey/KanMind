"""Views for boards."""

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.api.serializers import UserSummarySerializer
from auth_app.models import User
from boards_app.models import Board

from .permissions import IsBoardOwner, IsBoardOwnerOrMember
from .serializers import (
    BoardDetailSerializer,
    BoardSerializer,
    BoardUpdateSerializer,
    EmailCheckSerializer,
)


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


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Show, update or delete a single board."""

    # All boards, so the permission can answer 403 (not 404) for strangers.
    queryset = Board.objects.all()
    lookup_url_kwarg = "board_id"
    http_method_names = ["get", "patch", "delete", "head", "options"]

    def get_serializer_class(self):
        """Use the update serializer for PATCH, the detail one otherwise."""
        if self.request.method == "PATCH":
            return BoardUpdateSerializer
        return BoardDetailSerializer

    def get_permissions(self):
        """Allow only the owner to delete, members may read and update."""
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsBoardOwner()]
        return [IsAuthenticated(), IsBoardOwnerOrMember()]


class EmailCheckView(APIView):
    """Return the user registered with the given email address."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Validate the email parameter and look up the matching user."""
        params = EmailCheckSerializer(data=request.query_params)
        params.is_valid(raise_exception=True)
        # iexact: Max@Example.com finds max@example.com.
        user = get_object_or_404(
            User, email__iexact=params.validated_data["email"]
        )
        return Response(UserSummarySerializer(user).data)