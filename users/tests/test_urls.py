from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


class TestLoginUrls(TestCase):
    """ログイン時のアクセス"""

    def setUp(self):
        User = get_user_model()
        self.test_user = User.objects.create_user(email="test_user@test.com", password="test_user@test.com")
        self.client.force_login(self.test_user)

    def test_login_url(self):
        res = self.client.get(reverse("login"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "registration/login.html")

    def test_logout_url(self):
        res = self.client.get(reverse("logout"))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse("login"))

    def test_password_change_url(self):
        res = self.client.get(reverse("password_change"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "registration/password_change_form.html")

    def test_password_change_done_url(self):
        res = self.client.get(reverse("password_change_done"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "registration/password_change_done.html")

    def test_password_reset_url(self):
        """パスワード再設定 メール送信"""
        res = self.client.get(reverse("password_reset"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "registration/password_reset_form.html")

    def test_password_reset_done_url(self):
        """パスワード再設定 メール送信完了"""
        res = self.client.get(reverse("password_reset_done"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "registration/password_reset_done.html")

    # 実際の操作でアクセスするとURLが　http://127.0.0.1:8000/accounts/reset/Mg/set-password/になる
    def test_password_reset_confirm_get(self):
        """パスワード再設定フォーム"""
        # self.token = PasswordResetTokenGenerator().make_token(self.test_user)
        # urlsafe_b64encode：渡されたバイト文字列を安全なBase64形式にエンコードする　　force_bytes:ユーザーのプライマリキーをバイト文字列に変換
        self.uid = urlsafe_base64_encode(force_bytes(self.test_user.pk))
        self.token = default_token_generator.make_token(self.test_user)
        url = reverse("password_reset_confirm",
                      kwargs={
                          "uidb64": self.uid,
                          "token": self.token})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 302)
        redirect_url = reverse("password_reset_confirm",
                               kwargs={
                                   "uidb64": self.uid,
                                   "token": "set-password"})
        self.assertRedirects(res, redirect_url)

    def test_password_reset_confirm_post(self):
        self.uid = urlsafe_base64_encode(force_bytes(self.test_user.pk))
        self.token = default_token_generator.make_token(self.test_user)
        # PasswordResetConfirmViewはget時にトークンをsessionに保存し、post時にsessionのトークンをチェックしているため
        # 初めにgetリクエストを投げる
        get_url = reverse("password_reset_confirm",
                          kwargs={
                              "uidb64": self.uid,
                              "token": self.token})
        self.client.get(get_url)
        # 次にpoatを投げる
        # SetPasswordFormのフィールドはnew_passwordになっている
        post_data = {
            "new_password1": "reset_password",
            "new_password2": "reset_password"
        }
        url = reverse("password_reset_confirm",
                      kwargs={
                          "uidb64": self.uid,
                          "token": "set-password"})
        res = self.client.post(url, post_data)
        self.assertRedirects(res, reverse("password_reset_complete"))

    def test_password_reset_complete_url(self):
        """パスワード再設定 完了"""
        res = self.client.get(reverse("password_reset_complete"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "registration/password_reset_complete.html")


class TestLogoutAccess(TestCase):
    def test_login_url(self):
        res = self.client.get(reverse("login"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "registration/login.html")

    def test_logout_url(self):
        res = self.client.get(reverse("logout"))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse("login")+"?next=/accounts/logout/")

    def test_password_change_url(self):
        res = self.client.get(reverse("password_change"))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse("login")+"?next=/accounts/password_change/")

    def test_password_change_done_url(self):
        res = self.client.get(reverse("password_change_done"))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse("login")+"?next=/accounts/password_change/done/")

    def test_password_reset_url(self):
        """パスワード再設定 メール送信"""
        res = self.client.get(reverse("password_reset"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "registration/password_reset_form.html")

    def test_password_reset_done_url(self):
        """パスワード再設定 メール送信完了"""
        res = self.client.get(reverse("password_reset_done"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "registration/password_reset_done.html")

    def test_password_reset_confirm_url(self):
        """パスワード再設定"""
        User = get_user_model()
        test_user = User.objects.create_user(email="test_user@test.com", password="password_test")

        uid = urlsafe_base64_encode(force_bytes(test_user.pk))
        token = default_token_generator.make_token(test_user)
        get_url = reverse("password_reset_confirm",
                          kwargs={"uidb64": uid,
                                  "token": token})

        res = self.client.get(get_url)

        url = reverse("password_reset_confirm",
                      kwargs={
                          "uidb64": uid,
                          "token": "set-password"})
        self.assertRedirects(res, url)

    def test_password_reset_complete_url(self):
        """パスワード再設定 完了"""
        res = self.client.get(reverse("password_reset_complete"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "registration/password_reset_complete.html")
