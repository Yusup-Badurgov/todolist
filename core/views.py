
from rest_framework.generics import CreateAPIView

from core.models import User
from core.serializers import UserSerializer


class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
