"""URL routes of the boards app, mounted under /api/ in core/urls.py."""

from django.urls import path

from .views import BoardListCreateView

urlpatterns = [
    path('boards/', BoardListCreateView.as_view(), name='board-list'),
]