from django.db import transaction
from rest_framework import filters
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.models import Board, Goal
from goals.permissions import BoardPermissions
from goals.serializers import BoardCreateSerializer, BoardSerializer, BoardListSerializer


class BoardCreateView(CreateAPIView):
    """
    Представление для создания новой доски.
    Позволяет создать новую доску с использованием сериализатора BoardCreateSerializer.
    """

    model: Board = Board
    permission_classes: list = [IsAuthenticated]
    serializer_class: BoardCreateSerializer = BoardCreateSerializer


class BoardView(RetrieveUpdateDestroyAPIView):
    """
    Представление для просмотра, обновления и удаления доски.
    Позволяет получить, обновить и удалить доску с использованием сериализатора BoardSerializer.
    """

    model: Board = Board
    permission_classes: list = [IsAuthenticated, BoardPermissions]
    serializer_class: BoardSerializer = BoardSerializer

    def get_queryset(self):
        """
        Возвращает queryset досок, к которым пользователь имеет доступ.
        Фильтрация осуществляется по полю participants, где пользователь является участником.
        """
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board) -> Board:
        """
        Выполняет удаление доски.
        При удалении доски помечает ее как is_deleted, а также «удаляет» связанные с ней категории
        и обновляет статус целей.
        """
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)
        return instance


class BoardListView(ListAPIView):
    """
    Представление для просмотра списка всех досок.
    Позволяет получить список всех досок, к которым пользователь имеет доступ,
    с использованием сериализатора BoardListSerializer.
    """

    model: Board = Board
    permission_classes: list = [IsAuthenticated]
    pagination_class: LimitOffsetPagination = LimitOffsetPagination
    serializer_class: BoardListSerializer = BoardListSerializer
    filter_backends: list = [filters.OrderingFilter]
    ordering: list = ["title"]

    def get_queryset(self):
        """
        Возвращает queryset досок, к которым пользователь имеет доступ.
        Фильтрация осуществляется по полю participants, где пользователь является участником.
        """
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)
