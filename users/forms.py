from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # カスタムユーザーを使用
        model = User
        fields = ("email",)
