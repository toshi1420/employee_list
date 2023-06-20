from datetime import date
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


from employee_list_app.models import Employee, Branch

User = get_user_model()


class TestIndex(TestCase):
    def setUp(self):
        self.b = Branch.objects.create(name="a", address="aa", tel="1234567890")
        self.emp = Employee.objects.create(emp_id=10000, name="上野", post="python",
                                           date_of_entry=date(2010, 12, 31), branch=self.b)
        User.objects.create_user(email="test@test.com", password="test_user123")
        self.client.login(email="test@test.com", password="test_user123")

    def test_get(self):
        """GETアクセス時ステータスコード200かつ、データが表示されているか
        """
        url = reverse("index")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "employee_list/index.html")
        self.assertContains(res, 10000)
        self.assertContains(res, "上野")
        self.assertContains(res, "python")
        self.assertContains(res, "2010年12月31日")
        self.assertContains(res, "a")


class TsetEmpAdd(TestCase):
    def setUp(self):
        self.b = Branch.objects.create(name="a", address="aa", tel="1234567890")
        User.objects.create_user(email="test@test.com", password="test_user123")
        self.client.login(email="test@test.com", password="test_user123")

    def test_get(self):
        """GETアクセス時employee_list/emp_add.htmlが使われてるか
        """
        url = reverse("emp_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "employee_list/emp_add.html")

    def test_post(self):
        """社員追加しリダイレクトしているか
        """
        post_data = {"emp_id": 10001, "name": "野", "post": "py", "date_of_entry": "2011-12-31", "branch": self.b.pk}
        url = reverse("emp_add")
        res = self.client.post(url, post_data)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, url)
        self.assertTrue(Employee.objects.filter(emp_id=10001).exists())


class TestEmpEdit(TestCase):
    def setUp(self):
        self.bn = Branch.objects.create(name="長野支社", address="aa", tel="1234567890")
        self.bt = Branch.objects.create(name="東京本社", address="bb", tel="1234567890")
        self.edit_emp = Employee.objects.create(emp_id=10002, name="佐藤", post="python",
                                                date_of_entry=date(2010, 12, 31), branch=self.bn)
        User.objects.create_user(email="test@test.com", password="test_user123")
        self.client.login(email="test@test.com", password="test_user123")

    def test_get(self):
        """GETアクセス時ステータスコードが200か
        """
        url = reverse("emp_edit", kwargs={"pk": self.edit_emp.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "employee_list/emp_edit.html")
        self.assertContains(res, self.edit_emp.emp_id)
        self.assertContains(res, self.edit_emp.name)
        self.assertContains(res, self.edit_emp.post)
        self.assertContains(res, self.edit_emp.date_of_entry.year)
        self.assertContains(res, self.edit_emp.date_of_entry.month)
        self.assertContains(res, self.edit_emp.date_of_entry.day)
        self.assertContains(res, self.edit_emp.branch)

    def test_emp_edit(self):
        edit_data = {"emp_id": 10100, "name": "山田", "post": "",
                     "date_of_entry": date(2011, 10, 10), "branch": self.bt.pk}
        url = reverse("emp_edit", kwargs={"pk": self.edit_emp.pk})
        res = self.client.post(url, edit_data)
        edit_emp = Employee.objects.get(pk=self.edit_emp.pk)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse("index"))
        self.assertEqual(edit_emp.emp_id, 10100)
        self.assertEqual(edit_emp.name, "山田")
        self.assertEqual(edit_emp.post, None)
        self.assertEqual(edit_emp.date_of_entry, date(2011, 10, 10))
        self.assertEqual(edit_emp.branch, self.bt)

    def test_404(self):
        url = reverse("emp_edit", kwargs={"pk": 100})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)


class TestEmpDelete(TestCase):
    def setUp(self):
        self.b = Branch.objects.create(name="a", address="aa", tel="1234567890")
        self.delete_emp = Employee.objects.create(
            emp_id=10003, name="a", post="", date_of_entry=date(2010, 12, 31), branch=self.b)
        User.objects.create_user(email="test@test.com", password="test_user123")
        self.client.login(email="test@test.com", password="test_user123")

    def test_get(self):
        url = reverse("emp_delete", kwargs={"pk": self.delete_emp.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 405)

    def test_delete(self):
        url = reverse("emp_delete", kwargs={"pk": self.delete_emp.pk})
        res = self.client.post(url)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse("index"))
        self.assertFalse(Employee.objects.filter(emp_id=10003).exists())

    def test_404(self):
        url = reverse("emp_delete", kwargs={"pk": 100})
        res = self.client.post(url)
        self.assertEqual(res.status_code, 404)


class TestBranchView(TestCase):
    def setUp(self):
        Branch.objects.create(name="a", address="aa", tel="1234567890")
        User.objects.create_user(email="test@test.com", password="test_user123")
        self.client.login(email="test@test.com", password="test_user123")

    def test_get(self):
        res = self.client.get(reverse("branch_view"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "employee_list/branch_view.html")
        self.assertContains(res, "a")
        self.assertContains(res, "aa")
        self.assertContains(res, "1234567890")


class TestBranchEdit(TestCase):
    def setUp(self):
        self.edit_b = Branch.objects.create(name="edit_b", address="edit_b", tel="1234567890")
        User.objects.create_user(email="test@test.com", password="test_user123")
        self.client.login(email="test@test.com", password="test_user123")

    def test_get(self):
        url = reverse("branch_edit", kwargs={"pk": self.edit_b.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "employee_list/branch_edit.html")
        self.assertContains(res, self.edit_b.name)
        self.assertContains(res, self.edit_b.address)
        self.assertContains(res, self.edit_b.tel)

    def test_edit(self):
        url = reverse("branch_edit", kwargs={"pk": self.edit_b.pk})
        edit_data = {"name": "edit_b2", "address": "edit_b2", "tel": "12345678901"}
        res = self.client.post(url, edit_data)
        edit_brn = Branch.objects.get(pk=self.edit_b.pk)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse("index"))
        self.assertEqual(edit_brn.name, "edit_b2")
        self.assertEqual(edit_brn.address, "edit_b2")
        self.assertEqual(edit_brn.tel, "12345678901")

    def test_404(self):
        url = reverse("branch_edit", kwargs={"pk": 100})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)


class TestBranchAdd(TestCase):
    def setUp(self):
        User.objects.create_user(email="test@test.com", password="test_user123")
        self.client.login(email="test@test.com", password="test_user123")

    def test_get(self):
        res = self.client.get(reverse("branch_add"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "employee_list/branch_add.html")

    def test_branch_add(self):
        url = reverse("branch_add")
        post_data = {"name": "post_b", "address": "post_b", "tel": "12345678901"}
        res = self.client.post(url, post_data)
        self.assertTrue(Branch.objects.filter(name="post_b").exists())
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse("index"))


class TestBranchDelete(TestCase):
    def setUp(self):
        self.delete_b = Branch.objects.create(name="delete_b", address="delete_b", tel="1234567890")
        User.objects.create_user(email="test@test.com", password="test_user123")
        self.client.login(email="test@test.com", password="test_user123")

    def test_delete(self):
        url = reverse("branch_delete", kwargs={"pk": self.delete_b.pk})
        res = self.client.post(url)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse("index"))
        self.assertFalse(Branch.objects.filter(name="delete_b").exists())

    def test_404(self):
        url = reverse("branch_delete", kwargs={"pk": 100})
        res = self.client.post(url)
        self.assertEqual(res.status_code, 404)
