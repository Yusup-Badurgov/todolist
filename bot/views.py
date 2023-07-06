from django.conf import settings
from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from bot.models import TgUser
from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient


class VerificationView(GenericAPIView):
    model: TgUser = TgUser
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: TgUserSerializer = TgUserSerializer

    def patch(self, request, *args, **kwargs) -> Response:
        """
        Обновляет связанный объект TgUser с пользователем и отправляет сообщение в Telegram.

        Метод получает данные из запроса и выполняет валидацию с использованием сериализатора TgUserSerializer.
        Если данные валидны, связанный объект TgUser обновляется, связывается с пользователем,
        и отправляется сообщение в Telegram через TgClient.

        Args:
            request (Request): HTTP-запрос.
            *args: Дополнительные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            Response: Ответ HTTP.

        """
        s: TgUserSerializer = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)

        tg_user: TgUser = s.validated_data["tg_user"]
        tg_user.user = self.request.user
        tg_user.save(update_fields=["user"])
        instance_s: TgUserSerializer = self.get_serializer(tg_user)
        tg_client: TgClient = TgClient(settings.BOT_TOKEN)
        tg_client.send_message(tg_user.chat_id, "[verification has been completed]")

        return Response(instance_s.data)
