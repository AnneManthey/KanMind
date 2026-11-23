from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    """Custom User Model for login with email and fullname."""
    
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=150)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']
    objects = UserManager()

    def __str__(self):
        """Return email."""
        return self.email