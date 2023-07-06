from django.db import transaction
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.models import GoalCategory, Goal
from goals.permissions import GoalCategoryPermissions
from goals.serializers import GoalCategorySerializer, GoalCategoryCreateSerializer


class GoalCategoryCreateView(CreateAPIView):
    """
    Представление для создания новой категории целей.
    Позволяет создать новую категорию целей с использованием сериализатора GoalCategoryCreateSerializer.
    """

    model: GoalCategory = GoalCategory
    permission_classes: list = [IsAuthenticated]
    serializer_class: GoalCategoryCreateSerializer = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    """
    Представление для просмотра списка всех категорий целей.
    Позволяет получить список всех категорий целей, к которым пользователь имеет доступ,
    с использованием сериализатора GoalCategorySerializer.
    """

    model: GoalCategory = GoalCategory
    permission_classes: list = [IsAuthenticated]
    serializer_class: GoalCategorySerializer = GoalCategorySerializer
    pagination_class: LimitOffsetPagination = LimitOffsetPagination
    filter_backends: list = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields: list = ["title", "created"]
    filterset_fields: list = ["board", "user"]
    ordering: list = ["title"]
    search_fields: list = ["title"]

    def get_queryset(self) -> QuerySet[GoalCategory]:
        """
        Возвращает queryset категорий целей, к которым пользователь имеет доступ.
        Фильтрация осуществляется по полю board, где пользователь является участником,
        и исключаются удаленные категории.
        """
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    """
    Представление для просмотра, обновления и удаления категории целей.
    Позволяет получить, обновить и удалить категорию целей с использованием сериализатора GoalCategorySerializer.
    """

    model: GoalCategory = GoalCategory
    serializer_class: GoalCategorySerializer = GoalCategorySerializer
    permission_classes: list = [IsAuthenticated, GoalCategoryPermissions]

    def get_queryset(self) -> QuerySet[GoalCategory]:
        """
        Возвращает queryset категорий целей, к которым пользователь имеет доступ.
        Исключаются удаленные категории.
        """
        return GoalCategory.objects.filter(board__participants__user=self.request.user).exclude(is_deleted=True)

    def perform_destroy(self, instance: GoalCategory) -> GoalCategory:
        """
        Выполняет удаление категории целей.
        При удалении категории помечает ее как is_deleted и обновляет статус всех связанных целей на "archived".
        """
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            Goal.objects.filter(category=instance).update(status=Goal.Status.archived)
        return instance
