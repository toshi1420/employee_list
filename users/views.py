from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.contrib import messages

from .forms import SignupForm


class SignupView(SuccessMessageMixin, CreateView):
    """ form_validがない場合は、ユーザー登録後は、ログイン画面にリダイレクトさせ、
    ユーザーに手動でログインさせることになる """
    template_name = "registration/signup.html"
    form_class = SignupForm
    # classの中ではreverse_lazyじゃないとエラーになる
    success_url = reverse_lazy("index")
    success_message = "登録が完了しました"

    def form_valid(self, form):
        """ ユーザー登録後に自動でログインさせる """
        login(self.request, self.object)
        return super().form_valid(form)


class CustomLoginView(LoginView):

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        messages.success(self.request, f'"{username}" ログインしました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'ログインに失敗しました。正しいメールアドレスとパスワードを入力してください。')
        return super().form_invalid(form)
