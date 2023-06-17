from django.contrib.auth import login
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from core.models import User
from core.serializers import UserSerializer, LoginSerializer, UserProfileSerializer, ChangePasswordSerializer


class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginViews(CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request=request, user=user)
        return Response(serializer.data)


from rest_framework.generics import RetrieveUpdateDestroyAPIView
from django.contrib.auth import logout


class UserProfileView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        # Выполняем выход пользователя
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
