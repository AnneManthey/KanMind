"""Database models for boards."""

from django.conf import settings
from django.db import models


class Board(models.Model):
    """A Kanban board with one owner and any number of members."""

    title = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_boards",
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="member_boards",
    )

    class Meta:
        verbose_name = "board"
        verbose_name_plural = "boards"
        ordering = ["id"]

    def __str__(self):
        """Return the board title."""
        return self.title
