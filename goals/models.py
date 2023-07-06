from django.db import models
from django.utils import timezone

from core.models import User


class GoalCategory(models.Model):
    """
    Модель категории цели.
    Связана с моделью `Board` через внешний ключ `board`.
    Содержит информацию о названии, авторе, флаге удаления, дате создания и дате последнего обновления.
    """
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    board = models.ForeignKey('Board', verbose_name="Доска", on_delete=models.PROTECT, related_name="categories")
    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")

    def save(self, *args, **kwargs):
        """
        Переопределение метода save для автоматического проставления даты создания и обновления.
        """
        if not self.id:  # Когда объект только создается, у него еще нет id
            self.created = timezone.now()  # проставляем дату создания
        self.updated = timezone.now()  # проставляем дату обновления
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Goal(models.Model):
    """
    Модель цели.
    Содержит информацию о статусе, приоритете, авторе, категории, заголовке, описании и дате выполнения.
    """
    class Status(models.IntegerChoices):
        to_do = 1, "К выполнению"
        in_progress = 2, "В процессе"
        done = 3, "Выполнено"
        archived = 4, "Архив"

    class Priority(models.IntegerChoices):
        low = 1, "Низкий"
        medium = 2, "Средний"
        high = 3, "Высокий"
        critical = 4, "Критический"

    status = models.PositiveSmallIntegerField(verbose_name="Статус", choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(verbose_name="Приоритет", choices=Priority.choices,
                                                default=Priority.medium)
    user = models.ForeignKey(User, verbose_name="Автор", related_name="goals", on_delete=models.PROTECT)
    category = models.ForeignKey(GoalCategory, verbose_name="Категория", on_delete=models.PROTECT)
    title = models.CharField(verbose_name="Заголовок цели", max_length=255)
    description = models.TextField(verbose_name="Описание", null=True, blank=True, default=None)
    due_date = models.DateField(verbose_name="Дата выполнения", null=True, blank=True, default=None)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"


class GoalComment(models.Model):
    """
    Модель комментария к цели.
    Содержит информацию о тексте, цели, пользователе, дате создания и дате последнего обновления.
    """
    text = models.TextField(verbose_name="Текст")
    goal = models.ForeignKey(Goal, verbose_name="Цель", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Пользователь", related_name="comments", on_delete=models.PROTECT)
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=True)

    def __str__(self):
        return 'Comment #{}'.format(self.id)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Board(models.Model):
    """
    Модель доски.
    Содержит информацию о названии, флаге удаления, дате создания и дате последнего обновления.
    """
    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"

    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=True)

    def __str__(self):
        return '{}'.format(self.title)


class BoardParticipant(models.Model):
    """
    Модель участника доски.
    Связывает модели `Board` и `User` через внешние ключи `board` и `user`.
    Содержит информацию о роли участника, дате создания и дате последнего обновления.
    """
    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    class Role(models.IntegerChoices):
        owner = 1, "Владелец"
        writer = 2, "Редактор"
        reader = 3, "Читатель"

    board = models.ForeignKey(
        Board,
        verbose_name="Доска",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    role = models.PositiveSmallIntegerField(
        verbose_name="Роль", choices=Role.choices, default=Role.owner
    )

    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=True)

    def __str__(self):
        return '{}: {}'.format(self.board, self.user)
