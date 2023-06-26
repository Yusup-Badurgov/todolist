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
    model = Goal
    serializer_class = GoalCreateSerializer
    permission_classes = [IsAuthenticated]


class GoalDetailView(RetrieveUpdateDestroyAPIView):
    """ Модель представления, которая позволяет редактировать и удалять объекты Goal. """
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated, GoalPermissions]

    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user=self.request.user)

    def perform_destroy(self, instance):
        instance.status = Goal.Status.archived
        instance.save()
        return instance


class GoalListView(ListAPIView):
    """
    Модель представления, которая позволяет выводить все объекты Goal.
    Сортировать, фильтровать и искать по полям `title`, `description`
    """
    model = Goal
    permission_classes = [IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, ]
    filterset_class = GoalDateFilter
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "priority"]
    ordering = ["priority", "due_date"]

    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user=self.request.user)