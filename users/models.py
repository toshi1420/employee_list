from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Meta(AbstractUser.Meta):
        db_table = "custom_user"
        verbose_name_plural = "CustomUser"
