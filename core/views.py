from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from core.models import User
from core.serializers import UserSerializer, LoginSerializer, UserProfileSerializer, ChangePasswordSerializer


class UserRegistrationView(CreateAPIView):
    """
    Представление для регистрации нового пользователя.
    Позволяет создать нового пользователя с помощью сериализатора UserSerializer.
    """

    queryset: User.objects.all() = User.objects.all()
    serializer_class: UserSerializer = UserSerializer


class LoginViews(CreateAPIView):
    """
    Представление для аутентификации пользователя.
    Позволяет выполнить вход пользователя с помощью сериализатора LoginSerializer.
    """

    serializer_class: LoginSerializer = LoginSerializer
    permission_classes: list = [AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
        """
        Обрабатывает POST-запрос для выполнения входа пользователя.
        """
        serializer: LoginSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.save()
        login(request=request, user=user)
        return Response(serializer.data)


class UserProfileView(RetrieveUpdateDestroyAPIView):
    """
    Представление для просмотра, обновления и удаления профиля пользователя.
    Позволяет получить, обновить и удалить профиль пользователя с помощью сериализатора UserProfileSerializer.
    """

    queryset: User.objects.all() = User.objects.all()
    serializer_class: UserProfileSerializer = UserProfileSerializer
    permission_classes: list = [IsAuthenticated]

    def get_object(self) -> User:
        """
        Возвращает текущего пользователя.
        """
        return self.request.user

    def destroy(self, request, *args, **kwargs) -> Response:
        """
        Обрабатывает запрос на удаление профиля пользователя.
        Выполняет выход пользователя из системы.
        """
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(UpdateAPIView):
    """
    Представление для изменения пароля пользователя.
    Позволяет изменить пароль пользователя с помощью сериализатора ChangePasswordSerializer.
    """

    serializer_class: ChangePasswordSerializer = ChangePasswordSerializer
    permission_classes: list = [IsAuthenticated]

    def get_object(self) -> User:
        """
        Возвращает текущего пользователя.
        """
        return self.request.user
