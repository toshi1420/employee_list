from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import EmpListUser


class EmpListUserAdmin(UserAdmin):
    list_display = ("email", "is_staff", "is_superuser",)
    list_filter = ("is_staff", "is_superuser", "is_active",)
    filter_horizontal = ()
    ordering = ("email",)
    search_fields = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser",), },),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2"), },),
    )


# 管理サイトにカスタムユーザーモデルを登録
admin.site.register(EmpListUser, EmpListUserAdmin)
