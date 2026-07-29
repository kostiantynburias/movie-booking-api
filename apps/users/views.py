from rest_framework import generics, permissions

from apps.users.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for registering a new user.

    Allows unauthenticated users to create an account by providing
    an email and password.
    """

    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)