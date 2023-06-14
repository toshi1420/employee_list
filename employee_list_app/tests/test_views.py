from datetime import date
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


from employee_list_app.models import Employee, Branch

User = get_user_model()


class TestMixin(TestCase):
    def setUp(self):
        self.b = Branch.objects.create(name="a", address="aa", tel="1111")
        Employee.objects.create(emp_id=10000, name="上野", post="python", date_of_entry="2010-12-31", branch=self.b)
        user = User.objects.create_user(email="test_user@test.com", password="test_user123")
        self.client.force_login(user)


class TestIndex(TestMixin, TestCase):

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


class TsetEmpAdd(TestMixin, TestCase):

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
        add_data = {"emp_id": 10001, "name": "野", "post": "py", "date_of_entry": "2011-12-31", "branch": self.b.pk}
        url = reverse("emp_add")
        res = self.client.post(url, add_data)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, url)
        self.assertTrue(Employee.objects.filter(emp_id=10001).exists())


class TestEmpEdit(TestCase):
    def setUp(self):
        self.bn = Branch.objects.create(name="長野支社", address="aa", tel="1111")
        self.bt = Branch.objects.create(name="東京本社", address="bb", tel="2222")
        Employee.objects.create(emp_id=10000, name="佐藤", post="python", date_of_entry="2010-12-31", branch=self.bn)
        user = User.objects.create_user(email="test_user@test.com", password="test_user123")
        self.client.force_login(user)

    def test_get(self):
        """GETアクセス時ステータスコードが200か
        """
        emp = Employee.objects.get(emp_id=10000)
        url = reverse("emp_edit", kwargs={"pk": emp.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "employee_list/emp_edit.html")
        self.assertContains(res, emp.emp_id)
        self.assertContains(res, emp.name)
        self.assertContains(res, emp.post)
        self.assertContains(res, emp.date_of_entry.year)
        self.assertContains(res, emp.date_of_entry.month)
        self.assertContains(res, emp.date_of_entry.day)
        self.assertContains(res, emp.branch)

    def test_emp_edit(self):
        emp = Employee.objects.get(emp_id=10000)
        edit_data = {"emp_id": 10001, "name": "山田", "post": "", "date_of_entry": "2011-10-10", "branch": self.bt.pk}
        url = reverse("emp_edit", kwargs={"pk": emp.pk})
        res = self.client.post(url, edit_data)
        edit_emp = Employee.objects.get(pk=emp.pk)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse("index"))
        self.assertEqual(edit_emp.emp_id, 10001)
        self.assertEqual(edit_emp.name, "山田")
        self.assertEqual(edit_emp.post, None)
        self.assertEqual(edit_emp.date_of_entry, date(2011, 10, 10))
        self.assertEqual(edit_emp.branch, self.bt)

    def test_404(self):
        url = reverse("emp_edit", kwargs={"pk": 100})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)


class TestEmpDelete(TestMixin, TestCase):

    def test_get(self):
        emp = Employee.objects.get(emp_id=10000)
        url = reverse("emp_delete", kwargs={"pk": emp.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 405)

    def test_delete(self):
        emp = Employee.objects.get(emp_id=10000)
        url = reverse("emp_delete", kwargs={"pk": emp.pk})
        res = self.client.post(url)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse("index"))
        self.assertFalse(Employee.objects.filter(emp_id=1000).exists())

    def test_404(self):
        url = reverse("emp_delete", kwargs={"pk": 100})
        res = self.client.post(url)
        self.assertEqual(res.status_code, 404)


class TestBranchView(TestMixin, TestCase):

    def test_get(self):
        res = self.client.get(reverse("branch_view"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "employee_list/branch_view.html")
        self.assertContains(res, "a")
        self.assertContains(res, "aa")
        self.assertContains(res, "1111")


class TestBranchEdit(TestMixin, TestCase):

    def test_get(self):
        url = reverse("branch_edit", kwargs={"pk": self.b.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "employee_list/branch_edit.html")
        self.assertContains(res, self.b.name)
        self.assertContains(res, self.b.address)
        self.assertContains(res, self.b.tel)

    def test_edit(self):
        url = reverse("branch_edit", kwargs={"pk": self.b.pk})
        edit_data = {"name": "b", "address": "cc", "tel": "2222"}
        res = self.client.post(url, edit_data)
        edit_brn = Branch.objects.get(pk=self.b.pk)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse("index"))
        self.assertEqual(edit_brn.name, "b")
        self.assertEqual(edit_brn.address, "cc")
        self.assertEqual(edit_brn.tel, "2222")

    def test_404(self):
        url = reverse("branch_edit", kwargs={"pk": 100})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)


class TestBranchAdd(TestMixin, TestCase):

    def test_get(self):
        res = self.client.get(reverse("branch_add"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "employee_list/branch_add.html")

    def test_branch_add(self):
        url = reverse("branch_add")
        add_data = {"name": "b", "address": "aa", "tel": "2222"}
        res = self.client.post(url, add_data)
        self.assertTrue(Branch.objects.filter(name="b").exists())
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse("index"))


class TestBranchDelete(TestMixin, TestCase):

    def test_delete(self):
        url = reverse("branch_delete", kwargs={"pk": self.b.pk})
        res = self.client.post(url)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse("index"))
        self.assertFalse(Branch.objects.filter(name="a").exists())

    def test_404(self):
        url = reverse("branch_delete", kwargs={"pk": 100})
        res = self.client.post(url)
        self.assertEqual(res.status_code, 404)
