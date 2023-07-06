from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from core.models import User

# Убираем модель 'Group' из административного интерфейса
admin.site.unregister(Group)


# Регистрируем модель 'User' с настройками администратора
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Настраивает внешний вид и функциональность модели User в административном интерфейсе Django.
    """

    # Определяем поля, отображаемые в списке пользователей
    list_display = ("username", "first_name", "last_name", "email")

    # Определяем группировку полей для страницы редактирования пользователя
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ('Персональная информация', {"fields": ("first_name", "last_name", 'email')}),
        ('Права доступа', {"fields": ("is_active", "is_staff", 'is_superuser')}),
        ('Даты', {"fields": ("last_login", "date_joined")}),
    )
