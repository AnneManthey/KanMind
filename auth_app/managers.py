"""Custom manager for the e-mail based user model."""

from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Create users and superusers that log in with an e-mail address."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user.

        Args:
            email: Login address, must not be empty.
            password: Plain password, stored only as a hash.
            **extra_fields: Further model fields, e.g. ``fullname``.

        Returns:
            The saved user instance.

        Raises:
            ValueError: If no e-mail address is given.
        """
        if not email:
            raise ValueError("An e-mail address is required.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with staff rights.

        Raises:
            ValueError: If ``is_staff`` or ``is_superuser`` is not True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if not extra_fields["is_staff"] or not extra_fields["is_superuser"]:
            raise ValueError("A superuser needs is_staff and is_superuser.")
        return self.create_user(email, password, **extra_fields)