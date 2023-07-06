from django.db import transaction
from rest_framework import serializers

from core.models import User
from core.serializers import UserSerializer
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant
from django.core.exceptions import PermissionDenied


# _______________________________________________________________
# ________________goal_category_serializers______________________

class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания объектов модели GoalCategory.
    Проверяет, является ли пользователь владельцем или редактором доски, связанной с категорией цели.
    """

    user: serializers.HiddenField = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model: GoalCategory = GoalCategory
        fields: list = '__all__'
        read_only_fields: list = ["id", "created", "updated", "user"]

    def validate_board(self, value):
        """
        Проверяет, что доска, связанная с категорией, не удалена и пользователь является владельцем или редактором.
        """
        if value.is_deleted:
            raise serializers.ValidationError("Не разрешено в удаленном объекте")
        allow = BoardParticipant.objects.filter(
            board=value,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
            user=self.context["request"].user,
        ).exists()
        if not allow:
            raise serializers.ValidationError("Вы должны быть владельцем или редактором")
        return value


class GoalCategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода объектов модели GoalCategory.
    """

    user: UserSerializer = UserSerializer(read_only=True)

    class Meta:
        model: GoalCategory = GoalCategory
        fields: list = '__all__'
        read_only_fields: tuple = ("id", "created", "updated", "user", "board")


# _______________________________________________________________
# ________________goal_serializers_______________________________

class GoalCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания объектов модели Goal.
    Фильтрует, чтобы пользователь был владельцем категории, связанной с целью.
    """

    category: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(queryset=GoalCategory.objects.all())
    user: serializers.HiddenField = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model: Goal = Goal
        fields: list = '__all__'
        read_only_fields: list = ["id", "created", "updated", "user"]

    def validate_category(self, value):
        """
        Проверяет, что категория, связанная с целью, не удалена и пользователь является владельцем категории.
        """
        if value.is_deleted:
            raise serializers.ValidationError("Не разрешено в удаленной категории")

        if not BoardParticipant.objects.filter(
                board_id=value.board_id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                user=self.context["request"].user,
        ).exists():
            raise serializers.ValidationError("Вы не создавали эту категорию")
        return value


class GoalSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода объектов модели Goal.
    """

    user: UserSerializer = UserSerializer(read_only=True)

    class Meta:
        model: Goal = Goal
        fields: list = '__all__'
        read_only_fields: tuple = ("id", "created", "updated", "user")

    def validate_category(self, value):
        """
        Проверяет, что категория, связанная с целью, не удалена и пользователь является владельцем категории.
        """
        if value.is_deleted:
            raise serializers.ValidationError("Не разрешено в удаленной категории")

        if self.instance.category.board_id != value.board_id:
            raise serializers.ValidationError("Вы не создавали эту категорию")
        return value


# _______________________________________________________________
# ________________goal_comment_serializers_______________________________

class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания объектов модели GoalComment.
    Проверяет, является ли пользователь автором комментария.
    """

    user: serializers.HiddenField = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model: GoalComment = GoalComment
        fields: list = '__all__'
        read_only_fields: tuple = ("id", "created", "updated", "user")

    def validate_goal(self, value):
        """
        Проверяет, что пользователь является автором комментария.
        """
        if not BoardParticipant.objects.filter(
                board_id=value.category.board_id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                user=self.context["request"].user,
        ).exists():
            raise serializers.ValidationError("Вы не являетесь автором этого комментария")
        return value


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода объектов модели GoalComment.
    """

    user: UserSerializer = UserSerializer(read_only=True)

    class Meta:
        model: GoalComment = GoalComment
        fields: list = '__all__'
        read_only_fields: tuple = ("id", "created", "updated", "user", "goal")


# _______________________________________________________________
# ________________goal_board_serializers_______________________________

class BoardCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания объектов модели Board.
    """

    user: serializers.HiddenField = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model: Board = Board
        read_only_fields: tuple = ("id", "created", "updated")
        fields: str = "__all__"

    def create(self, validated_data):
        """
        Создает новую доску и добавляет пользователя в качестве владельца.
        """
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объектов модели BoardParticipant.
    """

    role: serializers.ChoiceField = serializers.ChoiceField(
        required=True, choices=BoardParticipant.Role.choices
    )
    user: serializers.SlugRelatedField = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model: BoardParticipant = BoardParticipant
        fields: str = "__all__"
        read_only_fields: tuple = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода объектов модели Board.
    """

    participants: BoardParticipantSerializer = BoardParticipantSerializer(many=True)
    user: serializers.HiddenField = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model: Board = Board
        fields: str = "__all__"
        read_only_fields: tuple = ("id", "created", "updated")

    def update(self, instance, validated_data):
        """
        Обновляет доску и роли участников доски.
        """
        owner = validated_data.pop("user")
        new_participants = validated_data.pop("participants")
        new_by_id = {part["user"].id: part for part in new_participants}

        old_participants = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in new_by_id:
                    old_participant.delete()
                else:
                    if old_participant.role != new_by_id[old_participant.user_id]["role"]:
                        old_participant.role = new_by_id[old_participant.user_id]["role"]
                        old_participant.save()
                    new_by_id.pop(old_participant.user_id)
            for new_part in new_by_id.values():
                BoardParticipant.objects.create(
                    board=instance, user=new_part["user"], role=new_part["role"]
                )

            instance.title = validated_data["title"]
            instance.save()

        return instance


class BoardListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода списка досок.
    """

    class Meta:
        model: Board = Board
        fields: str = "__all__"
