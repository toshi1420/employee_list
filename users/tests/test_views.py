from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

User = get_user_model()


class TestSignupView(TestCase):
    """getアクセス時、テンプレートがregistration/signup.htmlか？ステータスコードは200か？
    """

    def setUp(self):
        self.valid_data = {
            "email": "test1@test.com",
            "password1": "test_user123",
            "password2": "test_user123",
        }
        self.invalid_data = {
            "email": "test2@test.com",
            "password1": "test_user123",
            "password2": "invalid_password",
        }
        self.url = reverse("signup")

    def test_get(self):
        res = self.client.get(self.url)

        self.assertTemplateUsed(res, "registration/signup.html")
        self.assertEqual(res.status_code, 200)

    def test_valid(self):
        """postアクセス時、indexページにリダイレクトされるか？Userは登録されているか？
        """
        # POST後にリダイレクトを伴う場合、post()の引数にfollow = Trueを設定しておくと、リダイレクト先の情報がcontextなどに格納される
        res = self.client.post(self.url, self.valid_data)

        self.assertRedirects(res, reverse("index"))
        self.assertEqual(res.status_code, 302)

        self.assertTrue(User.objects.filter(email="test1@test.com").exists())
        user = User.objects.get(email=self.valid_data["email"])
        self.assertEqual(user.email, self.valid_data["email"])
        # ログインしているか？request.userを確認する
        self.assertTrue(res.wsgi_request.user.is_authenticated)
        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "登録が完了しました")

    def test_invalid(self):
        """バリデーション失敗時、signupページが表示されるか？Userは登録されていないか？
        """
        res = self.client.post(self.url, self.invalid_data)
        self.assertTemplateUsed(res, "registration/signup.html")
        self.assertEqual(res.status_code, 200)

        self.assertFalse(res.wsgi_request.user.is_authenticated)
        self.assertFalse(User.objects.filter(email="test2@test.com").exists())
        self.assertFormError(res, "form", "password2", "確認用パスワードが一致しません。")
        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "ユーザー登録に失敗しました。正しいメールアドレスとパスワードを入力してください。")


class TestCustomLoginView(TestCase):
    def setUp(self):
        self.url = reverse("login")
        self.user = User.objects.create_user(email="test@test.com", password="test_user123")

    def test_get(self):
        """getアクセス時、テンプレートがregistration/login.htmlか？ステータスコードは200か？
        """
        res = self.client.get(self.url)
        self.assertTemplateUsed(res, "registration/login.html")
        self.assertEqual(res.status_code, 200)
        # エラーメッセージが出ないことを確認
        self.assertFalse(res.context["form"].errors)

    def test_login_valid(self):
        """ログイン成功時、indexページにリダイレクトされ、ログイン状態になっているか？"""
        # POST後にリダイレクトを伴う場合、post()の引数にfollow = Trueを設定しておくと、リダイレクト先の情報がcontextなどに格納される
        res = self.client.post(self.url, {
            "username": "test@test.com",
            "password": "test_user123",
        }, follow=True)
        self.assertTemplateUsed(res, "employee_list/index.html")
        self.assertEqual(res.status_code, 200)
        # ログインしているか？
        self.assertTrue(res.wsgi_request.user.is_authenticated)
        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), '"test@test.com" ログインしました。')

    def test_login_invalid(self):
        """ログイン失敗時、ログインページが表示され、エラーメッセージが表示されるか？"""
        res = self.client.post(reverse("login"), {
            "email": "test2@test.com",
            "password": "invalid_password"
        })
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "registration/login.html")
        # ログインしていないか？
        self.assertFalse(res.wsgi_request.user.is_authenticated)
        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'ログインに失敗しました。正しいメールアドレスとパスワードを入力してください。')
