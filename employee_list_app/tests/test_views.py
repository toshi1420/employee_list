from datetime import date
from django.test import TestCase
from django.urls import reverse

from ..models import Employee, Branch


class TestIndex(TestCase):
    def setUp(self):
        b = Branch.objects.create(name="a", address="aa", tel="1111")
        Employee.objects.create(emp_id=10000, name="上野", post="python", date_of_entry="2010-12-31", branch=b)

    def test_get(self):
        """GETアクセス時ステータスコード200かつ、データが表示されているか
        """
        url = reverse("index")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 10000)
        self.assertContains(res, "上野")
        self.assertContains(res, "python")
        self.assertContains(res, "2010年12月31日")
        self.assertContains(res, "a")


class TsetEmpAdd(TestCase):
    def setUp(self):
        b = Branch.objects.create(name="a", address="aa", tel="1111")
        Employee.objects.create(emp_id=10000, name="上野", post="python", date_of_entry="2010-12-31", branch=b)

    def test_get(self):
        """GETアクセス時employee_list/emp_add.htmlが使われてるか
        """
        url = reverse("emp_add")
        res = self.client.get(url)
        self.assertTemplateUsed(res, "employee_list/emp_add.html")

    def test_post(self):
        """社員追加しリダイレクトしているか
        """
        b = Branch.objects.get(pk=1)
        add_data = {"emp_id": 10001, "name": "野", "post": "py", "date_of_entry": "2011-12-31", "branch": b.pk}
        url = reverse("emp_add")
        res = self.client.post(url, add_data)
        qs_counter = Employee.objects.count()
        self.assertEqual(res.status_code, 302)
        self.assertEqual(qs_counter, 2)


class TestEmpEdit(TestCase):
    def setUp(self):
        b1 = Branch.objects.create(name="長野支社", address="aa", tel="1111")
        Branch.objects.create(name="東京本社", address="bb", tel="2222")
        Employee.objects.create(emp_id=10000, name="佐藤", post="python", date_of_entry="2010-12-31", branch=b1)

    def test_get(self):
        """GETアクセス時ステータスコードが200か
        """
        emp = Employee.objects.get(emp_id=10000)
        url = reverse("emp_edit", kwargs={"pk": emp.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, emp.emp_id)
        self.assertContains(res, emp.name)
        self.assertContains(res, emp.post)
        self.assertContains(res, emp.date_of_entry)
        self.assertContains(res, emp.branch)

    def test_emp_edit(self):
        b2 = Branch.objects.get(name="東京本社")
        emp = Employee.objects.get(emp_id=10000)
        edit_data = {"emp_id": 10001, "name": "山田", "post": "", "date_of_entry": "2011-10-10", "branch": b2.pk}
        url = reverse("emp_edit", kwargs={"pk": emp.pk})
        res = self.client.post(url, edit_data)
        edit_emp = Employee.objects.get(pk=emp.pk)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(edit_emp.emp_id, 10001)
        self.assertEqual(edit_emp.name, "山田")
        self.assertEqual(edit_emp.post, None)
        self.assertEqual(edit_emp.date_of_entry, date(2011, 10, 10))
        self.assertEqual(edit_emp.branch, b2)

    def test_404(self):
        url = reverse("emp_edit", kwargs={"pk": 0})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)


class TestEmpDelte(TestCase):
    def setUp(self):
        b = Branch.objects.create(name="a", address="aa", tel="1111")
        Employee.objects.create(emp_id=10000, name="上野", post="python", date_of_entry="2010-12-31", branch=b)

    def test_get(self):
        emp = Employee.objects.get(emp_id=10000)
        url = reverse("emp_delete", kwargs={"pk": emp.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 405)

    def test_delete(self):
        emp = Employee.objects.get(emp_id=10000)
        url = reverse("emp_delete", kwargs={"pk": emp.pk})
        res = self.client.post(url)
        emp = Employee.objects.all()
        self.assertEqual(res.status_code, 302)
        self.assertEqual(emp.count(), 0)

    def test_404(self):
        url = reverse("emp_delete", kwargs={"pk": 0})
        res = self.client.post(url)
        self.assertEqual(res.status_code, 404)


class TestBranchView(TestCase):
    def setUp(self):
        b = Branch.objects.create(name="a", address="bb", tel="1111")
        Employee.objects.create(emp_id=10000, name="上野", post="python", date_of_entry="2010-12-31", branch=b)

    def test_get(self):
        res = self.client.get(reverse("branch_view"))
        self.assertTemplateUsed(res, "employee_list/branch_view.html")
        self.assertContains(res, "a")
        self.assertContains(res, "bb")
        self.assertContains(res, "1111")


class TestBranchEdit(TestCase):
    def setUp(self):
        Branch.objects.create(name="a", address="bb", tel="1111")

    def test_get(self):
        b = Branch.objects.get(name="a")
        url = reverse("branch_edit", kwargs={"pk": b.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, b.name)
        self.assertContains(res, b.address)
        self.assertContains(res, b.tel)

    def test_edit(self):
        b = Branch.objects.get(name="a")
        url = reverse("branch_edit", kwargs={"pk": b.pk})
        edit_data = {"name": "b", "address": "cc", "tel": "2222"}
        res = self.client.post(url, edit_data)
        edit_brn = Branch.objects.get(pk=b.pk)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(edit_brn.name, "b")
        self.assertEqual(edit_brn.address, "cc")
        self.assertEqual(edit_brn.tel, "2222")

    def test_404(self):
        url = reverse("branch_edit", kwargs={"pk": 0})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)


class TestBranchAdd(TestCase):
    def setUp(self):
        Branch.objects.create(name="a", address="bb", tel="1111")

    def test_get(self):
        res = self.client.get(reverse("branch_add"))
        self.assertTemplateUsed(res, "employee_list/branch_add.html")

    def test_branch_add(self):
        url = reverse("branch_add")
        add_data = {"name": "b", "address": "aa", "tel": "2222"}
        res = self.client.post(url, add_data)
        qs_counter = Branch.objects.count()
        self.assertEqual(qs_counter, 2)
        self.assertEqual(res.status_code, 302)


class TestBranchDelete(TestCase):
    def setUp(self):
        Branch.objects.create(name="a", address="bb", tel="1111")

    def test_delete(self):
        b = Branch.objects.get(name="a")
        url = reverse("branch_delete", kwargs={"pk": b.pk})
        res = self.client.post(url)
        brn = Branch.objects.all()
        self.assertEqual(res.status_code, 302)
        self.assertEqual(brn.count(), 0)

    def test_404(self):
        url = reverse("branch_delete", kwargs={"pk": 0})
        res = self.client.post(url)
        self.assertEqual(res.status_code, 404)
