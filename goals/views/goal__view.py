from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalDateFilter
from goals.models import Goal
from goals.serializers import GoalCreateSerializer, GoalSerializer


class GoalCreateView(CreateAPIView):
    serializer_class = GoalCreateSerializer
    permission_classes = [IsAuthenticated]


class GoalDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        instance.status = Goal.Status.archived  # Перемещаем цель в статус "Архив"
        instance.save()
        return None


class GoalListView(ListAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title", "description"]
    filterset_class = GoalDateFilter

    def get_queryset(self):
        queryset = Goal.objects.filter(user=self.request.user)
        return queryset
