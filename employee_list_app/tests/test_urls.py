from django.shortcuts import resolve_url
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from employee_list_app.models import Branch, Employee

User = get_user_model()


class TestMixin(TestCase):
    def setUp(self):
        self.client = Client()
        b = Branch.objects.create(name="a", address="aa", tel="1111")
        self.emp = Employee.objects.create(emp_id=10000, name="上野", post="python",
                                           date_of_entry="2010-12-31", branch=b)
        # test用アカウント作成
        self.test_user = User.objects.create_user(email="test_user@test.com", password="test_user@test.com")
        # ログイン
        self.client.login(username="test_user@test.com", password="test_user@test.com")


class TestLoginUrls(TestMixin, TestCase):
    """ログイン時アクセスできるかをテスト
    """

    def test_index_url(self):
        res = self.client.get(reverse("index"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "employee_list/index.html")

    def test_emp_add_url(self):
        res = self.client.get(reverse("emp_add"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "employee_list/emp_add.html")

    def test_emp_edit_url(self):
        res = self.client.get(reverse("emp_edit", kwargs={"pk": 1}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "employee_list/emp_edit.html")

    def test_emp_delete_url(self):
        Employee.objects.create(emp_id=10001, name="山田", post="engineer", date_of_entry="2022-01-01",
                                branch=Branch.objects.create(name="b", address="bb", tel="2222"))
        res = self.client.post(reverse("emp_delete", kwargs={"pk": 2}))
        self.assertEqual(res.status_code, 302)

    def test_branch_view_url(self):
        res = self.client.get(reverse("branch_view"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "employee_list/branch_view.html")

    def test_branch_add_url(self):
        res = self.client.get(reverse("branch_add"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "employee_list/branch_add.html")

    def test_branch_edit_url(self):
        res = self.client.get(reverse("branch_edit", kwargs={"pk": 1}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "employee_list/branch_edit.html")

    def test_branch_delete_url(self):
        Branch.objects.create(name="b", address="bb", tel="2222")
        res = self.client.post(reverse("branch_delete", kwargs={"pk": 2}))
        self.assertEqual(res.status_code, 302)


class TestRedirect(TestCase):
    """非ログイン時、ログインページにredirectされるか
    """

    def test_index_url(self):
        res = self.client.get(reverse("index"))
        res_url = resolve_url(res.url)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res_url, reverse("login")+"?next=/")

    def test_emp_add_url(self):
        res = self.client.get(reverse("emp_add"))
        res_url = resolve_url(res.url)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res_url, reverse("login")+"?next=/emp_add/")

    def test_emp_edit_url(self):
        res = self.client.get(reverse("emp_edit", kwargs={"pk": 1}))
        res_url = resolve_url(res.url)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res_url, reverse("login")+"?next=/emp_edit/1/")

    def test_emp_delete_url(self):
        Employee.objects.create(emp_id=10001, name="山田", post="engineer", date_of_entry="2022-01-01",
                                branch=Branch.objects.create(name="b", address="bb", tel="2222"))
        res = self.client.post(reverse("emp_delete", kwargs={"pk": 2}))
        res_url = resolve_url(res.url)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res_url, reverse("login")+"?next=/emp_delete/2/")

    def test_branch_view_url(self):
        res = self.client.get(reverse("branch_view"))
        res_url = resolve_url(res.url)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res_url, reverse("login")+"?next=/branch_view/")

    def test_branch_add_url(self):
        res = self.client.get(reverse("branch_add"))
        res_url = resolve_url(res.url)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res_url, reverse("login")+"?next=/branch_add/")

    def test_branch_edit_url(self):
        res = self.client.get(reverse("branch_edit", kwargs={"pk": 1}))
        res_url = resolve_url(res.url)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res_url, reverse("login")+"?next=/branch_edit/1/")

    def test_branch_delete_url(self):
        Branch.objects.create(name="b", address="bb", tel="2222")
        res = self.client.post(reverse("branch_delete", kwargs={"pk": 2}))
        res_url = resolve_url(res.url)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res_url, reverse("login")+"?next=/branch_delete/2/")
