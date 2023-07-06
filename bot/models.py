import random
import string

from django.db import models

from core.models import User

CODE_VOCABULARY: str = string.ascii_letters + string.digits


class TgUser(models.Model):
    """Минимальные поля в модели:
    - telegram chat_id
    - telegram user_ud
    - внутренний user_id пользователя (nullable поле)
    """
    chat_id: models.BigIntegerField = models.BigIntegerField(verbose_name='Чат ID')
    user_ud: models.BigIntegerField = models.BigIntegerField(verbose_name="user ud", unique=True)
    username: models.CharField = models.CharField(max_length=512, verbose_name="tg username", null=True, blank=True, default=None)
    user: models.ForeignKey = models.ForeignKey(User, models.PROTECT, null=True, blank=True, default=None,
                             verbose_name='Связанный пользователь')
    verification_code: models.CharField = models.CharField(max_length=12, verbose_name="Код подтверждения")

    def set_verification_code(self) -> None:
        """Устанавливает случайный код подтверждения длиной 12 символов."""
        code: str = "".join([random.choice(CODE_VOCABULARY) for _ in range(12)])
        self.verification_code = code

    def __str__(self) -> str:
        """Возвращает строковое представление модели."""
        return str(self.user)

    class Meta:
        verbose_name: str = "Телеграм Пользователь"
        verbose_name_plural: str = "Телеграм Пользователи"
