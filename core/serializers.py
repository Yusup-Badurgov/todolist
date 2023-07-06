from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.
    Используется для сериализации и десериализации данных пользователя.
    """

    password: serializers.CharField = serializers.CharField(required=True)
    password_repeat: serializers.CharField = serializers.CharField(write_only=True, required=True)

    class Meta:
        model: User = User
        fields: list = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat']
        extra_kwargs: dict = {
            'password': {'write_only': True},
        }

    def validate(self, data) -> dict:
        """
        Проверяет, что пароль и его повторение совпадают.
        """
        password: str = data.get('password')
        password_repeat: str = data.pop('password_repeat')

        if password != password_repeat:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data) -> User:
        """
        Создает и сохраняет нового пользователя.
        """
        password: str = validated_data.pop('password')
        user: User = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    """
    Сериализатор для аутентификации пользователя.
    """

    username: serializers.CharField = serializers.CharField(required=True)
    password: serializers.CharField = serializers.CharField(required=True, write_only=True)

    def create(self, validated_data) -> User:
        """
        Проверяет учетные данные пользователя и выполняет аутентификацию.
        """
        if not (user := authenticate(
                username=validated_data['username'],
                password=validated_data['password']
        )):
            raise AuthenticationFailed
        return user

    class Meta:
        model: User = User
        fields: str = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для профиля пользователя.
    Используется для сериализации данных профиля пользователя.
    """

    class Meta:
        model: User = User
        fields: list = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields: list = ['id']


class ChangePasswordSerializer(serializers.Serializer):
    """
    Сериализатор для изменения пароля пользователя.
    """

    old_password: serializers.CharField = serializers.CharField(required=True, write_only=True)
    new_password: serializers.CharField = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value) -> str:
        """
        Проверяет, что старый пароль введен правильно.
        """
        user: User = self.context['request'].user
        if not authenticate(username=user.username, password=value):
            raise serializers.ValidationError("Incorrect old password.")
        return value

    def validate_new_password(self, value) -> str:
        """
        Проверяет, что новый пароль отличается от старого пароля.
        """
        user: User = self.context['request'].user
        if user.check_password(value):
            raise serializers.ValidationError("New password must be different from the old password.")
        return value

    def update(self, instance, validated_data) -> User:
        """
        Изменяет пароль пользователя.
        """
        new_password: str = validated_data['new_password']
        instance.password = make_password(new_password)
        instance.save()
        return instance
