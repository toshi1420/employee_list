from django.test import TestCase

from employee_list_app.models import Branch

from ..forms import BranchForm, EmpForm, EmpSearchForm


class TestEmpForm(TestCase):
    def setUp(self):
        Branch.objects.create(name="長野支社", address="aa", tel="1111")

    def test_emp_form(self):
        b = Branch.objects.get(name="長野支社")
        test_emp = {"emp_id": 10001, "name": "a", "post": "", "date_of_entry": "2020-10-10", "branch":  b.pk}
        form = EmpForm(test_emp)
        self.assertTrue(form.is_valid())


class TestEmpSerchForm(TestCase):
    def test_emp_search_form(self):
        name = {"name": "a"}
        branch = {"branch": ""}
        form = EmpSearchForm(name, branch)
        self.assertTrue(form.is_valid())


class TestBranchForm(TestCase):
    def test_branch_form(self):
        b = {"name": "長野", "address": "bb", "tel": "22222"}
        form = BranchForm(b)
        self.assertTrue(form.is_valid())
