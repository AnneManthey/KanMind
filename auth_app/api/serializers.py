"""Serializers for registration and login."""

from rest_framework import serializers

from auth_app.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Validate registration data and create a new user."""

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("fullname", "email", "password", "repeated_password")
        extra_kwargs = {"password": {"write_only": True}}

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
