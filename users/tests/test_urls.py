from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model


class TestLoginUrls(TestCase):
    """ログイン時のアクセス"""

    def setUp(self):
        User = get_user_model()
        self.test_user = User.objects.create_user(email="test_user@test.com", password="test_user@test.com")
        self.client.login(email="test_user@test.com", password="test_user@test.com")

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
    def test_password_reset_confirm_url(self):
        """パスワード再設定フォーム"""
        token = PasswordResetTokenGenerator().make_token(self.test_user)
        res = self.client.get(reverse("password_reset_confirm", kwargs={
                              "uid64": self.test_user.pk, "token": "set-password"}))
        self.assertEqual(res.status_code, 302)
        self.assertTemplateUsed(res, "registration/password_reset_confirm.html")

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
        test_user = User.objects.create_user(email="test_user@test.com", password="test_user@test.com")
        token = PasswordResetTokenGenerator().make_token(test_user)
        res = self.client.get(reverse("password_reset_confirm", kwargs={"uid64": test_user.pk, "token": token}))
        self.assertEqual(res.status_code, 302)
        self.assertTemplateUsed(res, "registration/password_reset_confirm.html")

    def test_password_reset_complete_url(self):
        """パスワード再設定 完了"""
        res = self.client.get(reverse("password_reset_complete"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "registration/password_reset_complete.html")
