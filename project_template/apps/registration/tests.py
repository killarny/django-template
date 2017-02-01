from django.test import TestCase

from .models import User


class RegistrationTests(TestCase):
    def test_first_user_is_admin(self):
        """The first user (and only they) are automatically administrator."""
        user = User.objects.create(username='username', email='foo@bar.com')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        user = User.objects.create(username='username2', email='foo@bar.com')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
