"""URL routes for tasks."""

from django.urls import path

from .views import (
    AssignedToMeView,
    ReviewingView,
    TaskCreateView,
    TaskDetailView,
)

urlpatterns = [
    path("tasks/", TaskCreateView.as_view()),
    path("tasks/assigned-to-me/", AssignedToMeView.as_view()),
    path("tasks/reviewing/", ReviewingView.as_view()),
    path("tasks/<int:pk>/", TaskDetailView.as_view()),
]