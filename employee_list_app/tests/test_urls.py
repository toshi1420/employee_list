from django.test import TestCase
from django.urls import reverse, resolve

from employee_list_app.models import Branch, Employee
from ..views import index, emp_add, emp_edit, emp_delete, branch_view
from ..views import branch_add, branch_edit, branch_delete


class TestUrls(TestCase):
    """indexページへのURLでアクセスする時のリダイレクトをテスト
    """

    def setUp(self):
        b = Branch.objects.create(name="a", address="aa", tel="1111")

        Employee.objects.create(emp_id=10000, name="上野", post="python", date_of_entry="2010-12-31", branch=b)

    def test_index_url(self):
        url = reverse("index")
        self.assertEqual(resolve(url).func, index)

    def test_emp_add_url(self):
        url = reverse("emp_add")
        self.assertEqual(resolve(url).func, emp_add)

    def test_emp_edit_url(self):
        emp = Employee.objects.get(emp_id=10000)
        url = reverse("emp_edit", kwargs={"pk": emp.pk})
        self.assertEqual(resolve(url).func, emp_edit)

    def test_emp_delete(self):
        emp = Employee.objects.get(emp_id=10000)
        url = reverse("emp_delete", kwargs={"pk": emp.pk})
        self.assertEqual(resolve(url).func, emp_delete)

    def test_branch_view_url(self):
        url = reverse("branch_view")
        self.assertEqual(resolve(url).func, branch_view)

    def test_branch_add_url(self):
        url = reverse("branch_add")
        self.assertEqual(resolve(url).func, branch_add)

    def test_branch_edit_url(self):
        b = Branch.objects.get(name="a")
        url = reverse("branch_edit", kwargs={"pk": b.pk})
        self.assertEqual(resolve(url).func, branch_edit)

    def test_branch_delete(self):
        b = Branch.objects.get(name="a")
        url = reverse("branch_delete", kwargs={"pk": b.pk})
        self.assertEqual(resolve(url).func, branch_delete)
