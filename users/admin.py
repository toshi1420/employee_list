from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fiels": ("first_name", "last_name", "email")}),
        (_("permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permistions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


# 管理サイトにカスタムユーザーモデルを登録
admin.site.register(CustomUser,)
