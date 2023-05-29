from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin

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
        # self.objectにsave()されたUserオブジェクトが入る
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid
