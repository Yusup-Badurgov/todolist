from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    verification_code: serializers.CharField = serializers.CharField(write_only=True)

    class Meta:
        model: TgUser = TgUser
        read_only_fields: tuple = ("user_ud", "username", "user_id")
        fields: tuple = ("user_ud", "username", "verification_code", "user_id")

    def validate(self, attrs: dict) -> dict:
        """
        Проверяет корректность кода подтверждения и наличие связанного объекта TgUser.

        Если код подтверждения некорректен или не связанный объект TgUser не найден,
        генерируется исключение ValidationError.

        Args:
            attrs (dict): Атрибуты, полученные от сериализатора.

        Returns:
            dict: Валидированные атрибуты.

        Raises:
            ValidationError: Если код подтверждения некорректен или не найден объект TgUser.
        """
        verification_code: str = attrs.get("verification_code")
        tg_user: TgUser = TgUser.objects.filter(verification_code=verification_code).first()
        if not tg_user:
            raise ValidationError({"verification_code": "field is incorrect"})
        attrs["tg_user"] = tg_user
        return attrs
