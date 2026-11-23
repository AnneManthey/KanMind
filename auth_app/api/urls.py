"""URL routes of the auth app, mounted under /api/ in core/urls.py."""

from django.urls import path

from .views import RegistrationView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
]