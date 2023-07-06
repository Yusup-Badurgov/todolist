from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
       Пользовательская модель пользователя, наследующаяся от AbstractUser.
       """
    REQUIRED_FIELDS = []  # убрали необходимости вводя почты при создании superuser'a
