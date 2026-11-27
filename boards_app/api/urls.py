"""URL routes of the boards app, mounted under /api/ in core/urls.py."""

from django.urls import path

from .views import BoardDetailView, BoardListCreateView, EmailCheckView

urlpatterns = [
    path('boards/', BoardListCreateView.as_view(), name='board-list'),
    path(
        'boards/<int:board_id>/',
        BoardDetailView.as_view(),
        name='board-detail',
    ),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),
]
