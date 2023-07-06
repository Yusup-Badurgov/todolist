from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalDateFilter
from goals.models import Goal
from goals.permissions import GoalPermissions
from goals.serializers import GoalCreateSerializer, GoalSerializer


class GoalCreateView(CreateAPIView):
    """ Модель представления, которая позволяет создавать объект Goal """
    model: Goal = Goal
    serializer_class: GoalCreateSerializer = GoalCreateSerializer
    permission_classes: list = [IsAuthenticated]


class GoalDetailView(RetrieveUpdateDestroyAPIView):
    """ Модель представления, которая позволяет редактировать и удалять объекты Goal. """
    model: Goal = Goal
    serializer_class: GoalSerializer = GoalSerializer
    permission_classes: list = [IsAuthenticated, GoalPermissions]

    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user=self.request.user)

    def perform_destroy(self, instance: Goal) -> Goal:
        instance.status = Goal.Status.archived
        instance.save()
        return instance


class GoalListView(ListAPIView):
    """
    Модель представления, которая позволяет выводить все объекты Goal.
    Сортировать, фильтровать и искать по полям `title`, `description`
    """
    model: Goal = Goal
    permission_classes: list = [IsAuthenticated]
    serializer_class: GoalSerializer = GoalSerializer
    pagination_class: LimitOffsetPagination = LimitOffsetPagination
    filter_backends: list = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, ]
    filterset_class: GoalDateFilter = GoalDateFilter
    search_fields: list = ["title", "description"]
    ordering_fields: list = ["due_date", "priority"]
    ordering: list = ["priority", "due_date"]

    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user=self.request.user)
