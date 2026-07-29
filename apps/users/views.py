from rest_framework import generics, permissions

from apps.users.serializers import RegisterSerializer, ProfileSerializer


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for registering a new user.

    Allows unauthenticated users to create an account by providing
    an email and password.
    """

    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating the authenticated user's profile.
    """

    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """
        Return the current authenticated user.
        """
        return self.request.user