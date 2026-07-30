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


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user password.
    """

    old_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Старий пароль вказано неправильно.')
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({'new_password_confirm': 'Нові паролі не збігаються.'})
        return attrs