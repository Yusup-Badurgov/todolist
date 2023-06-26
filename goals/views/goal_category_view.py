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
    model = GoalCategory
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    """ Модель представления, которая позволяет просматривать все объекты Category """
    model = GoalCategory
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter, ]
    ordering_fields = ["title", "created"]
    filterset_fields = ["board", "user"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)



class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    """ Модель представления, которая позволяет редактировать и удалять объекты из Category """
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [IsAuthenticated, GoalCategoryPermissions]

    def get_queryset(self) -> QuerySet[GoalCategory]:
        return GoalCategory.objects.filter(board__participants__user=self.request.user).exclude(is_deleted=True)

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            Goal.objects.filter(category=instance).update(status=Goal.Status.archived)
        return instance
