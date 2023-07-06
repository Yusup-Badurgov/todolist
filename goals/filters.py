import django_filters
from django.db import models
from django_filters import rest_framework

from goals.models import Goal


class GoalDateFilter(rest_framework.FilterSet):
    """
    Фильтр для целей на основе даты.
    Позволяет фильтровать цели по полю `due_date`.
    """

    class Meta:
        model = Goal
        fields = {
            "due_date": ("lte", "gte"),  # Фильтрация по полю `due_date`. Доступные операторы: lte (меньше или равно), gte (больше или равно).
            "category": ("exact", "in"),  # Фильтрация по полю `category`. Доступные операторы: exact (равно), in (в списке значений).
            "status": ("exact", "in"),  # Фильтрация по полю `status`. Доступные операторы: exact (равно), in (в списке значений).
            "priority": ("exact", "in"),  # Фильтрация по полю `priority`. Доступные операторы: exact (равно), in (в списке значений).
        }

    filter_overrides = {
        models.DateTimeField: {"filter_class": django_filters.IsoDateTimeFilter},  # Использование `IsoDateTimeFilter` для поля `due_date` типа DateTimeField.
    }
