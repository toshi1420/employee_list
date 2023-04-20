from datetime import date
from django.test import TestCase
from employee_list_app.models import Employee, Branch


class EmployeeModelTests(TestCase):
    def setUp(self):
        b = Branch.objects.create(name="a", address="aa", tel="1111")
        Employee.objects.create(emp_id=10000, name="上野", post="python", date_of_entry="2010-12-31", branch=b)

    def test_is_count_one(self):
        """レコードが登録されているか
        """
        b = Branch.objects.create(name="a", address="aa", tel="1111")
        Employee.objects.create(emp_id=10001, name="ueno", post="py", date_of_entry="2012-12-31", branch=b)
        emp_count = Employee.objects.count()
        self.assertEqual(emp_count, 2)

    def test_saving_and_retrieving_emp(self):
        """内容を指定して保存したデータと、すぐに取り出したデータが同じ値か
        """
        emp = Employee()
        b = Branch.objects.get(name="a")
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


class BranchModelTest(TestCase):
    def setUp(self):
        Branch.objects.create(name="a", address="aa", tel="1111")

    def test_is_count_one(self):
        """レコードが登録されているか
        """
        Branch.objects.create(name="b", address="bb", tel="2222")
        b_count = Branch.objects.count()
        self.assertEqual(b_count, 2)

    def test_saveing_and_retrieving_brn(self):
        """内容を指定して登録したデータと、すぐにとり出したデータが同じ値か
        """
        b = Branch()
        name = "b"
        address = "bb"
        tel = "2222"
        b.name = name
        b.address = address
        b.tel = tel
        b.save()

        saved_b = Branch.objects.get(name="b")
        actual = saved_b
        self.assertEqual(actual.name, name)
        self.assertEqual(actual.address, address)
        self.assertEqual(actual.tel, tel)
