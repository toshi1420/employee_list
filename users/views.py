from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignupForm


class SignupView(CreateView):
    """ form_validがない場合は、ユーザー登録後は、ログイン画面にリダイレクトさせ、
    ユーザーに手動でログインさせることになる """
    template_name = "account/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        """ ユーザー登録後に自動でログインさせる """

        # self.objectにsave()されたUserオブジェクトが入る
        valid = super().form_valid(form)
        # user = form.save()
        login(self.request, self.get_object())
        return valid
