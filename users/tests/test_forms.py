from django.test import TestCase
from users.forms import SignupForm
from django.contrib.auth import get_user_model

User = get_user_model()


class TestSignupForm(TestCase):
    def test_signup_form_valid(self):
        form_data = {"email": "test_user@test.com", "password1": "fjdksla;", "password2": "fjdksla;"}
        form = SignupForm(data=form_data)
        self.assertTrue(form.is_valid())
