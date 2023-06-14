from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class TestEmpLsitUser(TestCase):
    def test_create(self):
        User.objects.create_user(email="test_user@test.com", password="test_user123")
        self.assertTrue(User.objects.filter(email="test_user@test.com").exists())

    def test_delete(self):
        user = User.objects.create_user(email="test_user@test.com", password="test_user123")
        user.delete()
        self.assertFalse(User.objects.filter(email="test_user@test.com").exists())

    def test_saveing_and_retrieving_user(self):
        """内容を指定して登録したデータと、すぐにとり出したデータが同じ値か
        """
        user = User()
        email = "test_user@test.com"
        password = "test_user123"
        user.email = email
        user.password = password
        user.save()

        actual_user = User.objects.filter(email=email).get()
        self.assertEqual(actual_user.email, email)
        self.assertEqual(actual_user.password, password)
