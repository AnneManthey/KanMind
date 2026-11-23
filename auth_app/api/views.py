"""Views for registration and login."""

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, RegistrationSerializer


def build_auth_response(user):
    """Build the response data shared by registration and login.

    Args:
        user: The authenticated or newly created user.

    Returns:
        A dict with the token, full name, e-mail and id of the user.
    """
    token, _ = Token.objects.get_or_create(user=user)
    return {
        "token": token.key,
        "fullname": user.fullname,
        "email": user.email,
        "user_id": user.id,
    }


class RegistrationView(APIView):
    """Register a new user and return an auth token."""

    permission_classes = [AllowAny]
    # Ignore any token header, so an old token cannot block this open endpoint.
    authentication_classes = []

    def post(self, request):
        """Create a user from the request data.

        Args:
            request: The request with fullname, email, password and
                repeated_password.

        Returns:
            Response with status 201 and the auth data of the new user.
        """
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            build_auth_response(user), status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    """Log a user in and return an auth token."""

    permission_classes = [AllowAny]
    # Ignore any token header, so an old token cannot block this open endpoint.
    authentication_classes = []

    def post(self, request):
        """Authenticate the user from the request data.

        Args:
            request: The request with email and password.

        Returns:
            Response with status 200 and the auth data of the user.
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return Response(build_auth_response(user))
