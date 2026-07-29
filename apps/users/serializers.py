from rest_framework import serializers

from apps.users.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    
    Handles user creation, ensuring password is properly hashed
    and excluded from API responses for security.
    """

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password']
        read_only_fields = ['id']


    def create(self, validated_data):
        """
        Creates and returns a new user with a hashed password.
        """
        user = CustomUser.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password')
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing and updating user profile.
    """

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'role']
        read_only_fields = ['id', 'email', 'role']