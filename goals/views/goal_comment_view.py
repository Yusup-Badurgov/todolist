from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.models import GoalComment
from goals.permissions import CommentPermissions
from goals.serializers import CommentCreateSerializer, CommentSerializer


class CommentCreateView(CreateAPIView):
    """ Модель представления, которая позволяет создавать объекты Comment. """
    model: GoalComment = GoalComment
    serializer_class: CommentCreateSerializer = CommentCreateSerializer
    permission_classes: list = [IsAuthenticated]


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    """ Модель представления, которая позволяет редактировать и удалять объекты Comment. """
    model: GoalComment = GoalComment
    serializer_class: CommentSerializer = CommentSerializer
    permission_classes: list = [IsAuthenticated, CommentPermissions]

    def get_queryset(self):
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)


class CommentListView(ListAPIView):
    """
    Модель представления, которая позволяет выводить все объекты Comment.
    Так же сортирую и делает фильтрацию по полю `goal`.
    """
    model: GoalComment = GoalComment
    serializer_class: CommentSerializer = CommentSerializer
    permission_classes: list = [IsAuthenticated]
    pagination_class: LimitOffsetPagination = LimitOffsetPagination
    filter_backends: list = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields: list = ["goal"]
    ordering: str = "-id"

    def get_queryset(self):
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)
