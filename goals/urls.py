from django.urls import path

from goals.views.goal__view import GoalCreateView, GoalDetailView, GoalListView
from goals.views.goal_category_view import GoalCategoryCreateView, GoalCategoryListView, GoalCategoryView
from goals.views.goal_comment_view import CommentCreateView, CommentListView, CommentDetailView

urlpatterns = [
    path("goal_category/create", GoalCategoryCreateView.as_view()),
    path("goal_category/list", GoalCategoryListView.as_view()),
    path("goal_category/<pk>", GoalCategoryView.as_view()),

    path("goal/create", GoalCreateView.as_view()),
    path("goal/list", GoalListView.as_view()),
    path("goal/<pk>", GoalDetailView.as_view()),

    path('goal_comment/create', CommentCreateView.as_view(), name='comment-create'),
    path('goal_comment/list', CommentListView.as_view(), name='comment-list'),
    path('goal_comment/<int:pk>', CommentDetailView.as_view(), name='comment-detail'),
]