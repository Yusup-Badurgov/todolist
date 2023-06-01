from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from core.models import User

# Register your models here.
admin.site.unregister(Group)  # убирает вкладку "Group' из админки


@admin.register(User)
class CstomUserAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "email")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ('Personal ingo', {"fields": ("first_name", "last_name", 'email')}),
        ('Permissions', {"fields": ("is_active", "is_staff", 'is_superuser')}),
        ('dates', {"fields": ("last_login", "date_joined")}),
    )
