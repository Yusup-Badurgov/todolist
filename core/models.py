from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    REQUIRED_FIELDS = [] # убрали необходимости вводя почты при создании superuser'a
