from django.contrib.auth.models import User
from django.core.mail import mail_managers


def first_user_is_admin(backend, user, response, *args, **kwargs):
    if (User.objects.count() == 1) and (User.objects.first().pk == user.pk):
        # this is the only user in the system, so give them full access
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        # tell the managers what just happened, via email
        mail_managers('New superuser now has full site access.',
                      'User "{username}" is the first user to sign up, and '
                      'has been automatically granted superuser access.')
