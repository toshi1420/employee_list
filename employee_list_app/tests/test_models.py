from datetime import date
from django.test import TestCase
from employee_list_app.models import Employee, Branch


class EmployeeModelTests(TestCase):
    def test_is_create(self):
        """レコードが登録されているか
        """
        b = Branch.objects.create(name="a", address="aa", tel="1111")
        Employee.objects.create(emp_id=10001, name="ueno", post="py", date_of_entry="2012-12-31", branch=b)
        self.assertTrue(Employee.objects.filter(emp_id=10001).exists())

    def test_saving_and_retrieving_emp(self):
        """内容を指定して保存したデータと、すぐに取り出したデータが同じ値か
        """
        emp = Employee()
        b = Branch.objects.create(name="a", address="aa", tel="1111")
        emp_id = 10100
        name = "a"
        post = "aa"
        date_of_entry = date(1999, 10, 10)
        branch = b
        emp.emp_id = emp_id
        emp.name = name
        emp.post = post
        emp.date_of_entry = date_of_entry
        emp.branch = branch
        emp.save()

        saved_emp = Employee.objects.get(emp_id=10100)
        acutal = saved_emp

        self.assertEqual(acutal.emp_id, emp_id)
        self.assertEqual(acutal.name, name)
        self.assertEqual(acutal.post, post)
        self.assertEqual(acutal.date_of_entry, date_of_entry)
        self.assertEqual(acutal.branch, branch)

    def test_is_delete(self):
        b = Branch.objects.create(name="a", address="aa", tel="1111")
        emp = Employee.objects.create(emp_id=10000, name="上野", post="python", date_of_entry="2010-12-31", branch=b)
        emp.delete()
        self.assertFalse(Employee.objects.filter(emp_id=10000).exists())


class BranchModelTest(TestCase):
    def test_is_create(self):
        """レコードが登録されているか
        """
        Branch.objects.create(name="b", address="bb", tel="2222")
        self.assertTrue(Branch.objects.filter(name="b").exists())

    def test_saveing_and_retrieving_brn(self):
        """内容を指定して登録したデータと、すぐにとり出したデータが同じ値か
        """
        b = Branch()
        name = "c"
        address = "cc"
        tel = "3333"
        b.name = name
        b.address = address
        b.tel = tel
        b.save()

        actual = Branch.objects.get(name="c")

        self.assertEqual(actual.name, name)
        self.assertEqual(actual.address, address)
        self.assertEqual(actual.tel, tel)

    def test_is_delete(self):
        b = Branch.objects.create(name="d", address="d", tel="4444")
        b.delete()
        self.assertFalse(Branch.objects.filter(name="d").exists())
