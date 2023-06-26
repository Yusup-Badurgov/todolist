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
    model = GoalComment
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    """ Модель представления, которая позволяет редактировать и удалять объекты Comment. """
    model = GoalComment
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, CommentPermissions]

    def get_queryset(self):
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)


class CommentListView(ListAPIView):
    """
    Модель представления, которая позволяет выводить все объекты Comment.
    Так же сортирую и делает фильтрацию по полю `goal`.
    """
    model = GoalComment
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["goal"]
    ordering = "-id"

    def get_queryset(self):
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)
