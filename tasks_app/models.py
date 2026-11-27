"""Database models for tasks and their comments."""

from django.conf import settings
from django.db import models


class Task(models.Model):
    """A task that belongs to one board."""

    class Status(models.TextChoices):
        """Allowed workflow states; values must match the API docs."""

        TO_DO = "to-do", "To do"
        IN_PROGRESS = "in-progress", "In progress"
        REVIEW = "review", "Review"
        DONE = "done", "Done"

    class Priority(models.TextChoices):
        """Allowed priorities; values must match the API docs."""

        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    board = models.ForeignKey(
        "boards_app.Board",
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TO_DO,
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewing_tasks",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_tasks",
    )
    due_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "task"
        verbose_name_plural = "tasks"
        ordering = ["id"]

    def __str__(self):
        """Return the task title."""
        return self.title


class Comment(models.Model):
    """A comment written by a user on a task."""

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"
        ordering = ["created_at"]

    def __str__(self):
        """Return a short label with author and task."""
        return f"Comment by {self.author} on {self.task}"
