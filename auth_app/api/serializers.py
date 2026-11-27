"""Serializers for registration and login."""

from django.contrib.auth import authenticate
from rest_framework import serializers

from auth_app.models import User


class UserSummarySerializer(serializers.ModelSerializer):
    """Show the public user data used inside boards and tasks."""

    class Meta:
        model = User
        fields = ("id", "email", "fullname")


class RegistrationSerializer(serializers.ModelSerializer):
    """Validate registration data and create a new user."""

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("fullname", "email", "password", "repeated_password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        """Reject an e-mail that exists in any spelling.

        Args:
            value: The e-mail that passed the field validation.

        Returns:
            The unchanged e-mail.

        Raises:
            serializers.ValidationError: If the e-mail is already taken.
        """
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value

    def validate(self, data):
        """Check that both passwords are identical.

        Args:
            data: The already field-validated input data.

        Returns:
            The unchanged input data.

        Raises:
            serializers.ValidationError: If the passwords differ.
        """
        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError(
                {"repeated_password": "Passwords do not match."}
            )
        return data

    def create(self, validated_data):
        """Create a user with a hashed password.

        Args:
            validated_data: The validated input data.

        Returns:
            The newly created user.
        """
        validated_data.pop("repeated_password")
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """Check e-mail and password and provide the matching user."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Authenticate the user with the given credentials.

        Args:
            data: The already field-validated input data.

        Returns:
            The input data extended by the authenticated ``user``.

        Raises:
            serializers.ValidationError: If the credentials are wrong.
        """
        user = authenticate(email=data["email"], password=data["password"])
        # One generic message, so nobody can find out which e-mails exist.
        if user is None:
            raise serializers.ValidationError("Invalid email or password.")
        data["user"] = user
        return data
