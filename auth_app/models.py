"""Custom user model that logs in with an e-mail address."""

from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    """Custom User Model for login with email and fullname."""

    # Setting an inherited field to None removes it from the model.
    username = None
    first_name = None
    last_name = None
    # Unique, because the e-mail address replaces the username as login.
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=150)
    # Field used to log in; createsuperuser also asks for REQUIRED_FIELDS.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']
    objects = UserManager()

    def __str__(self):
        """Return email."""
        return self.email
