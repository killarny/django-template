from django.contrib.auth.models import AbstractUser
from django.core.mail import mail_managers
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    def __str__(self):
        return self.get_full_name()

    @property
    def facebook(self):
        return self.social_auth.get(provider='facebook')

    @property
    def image_url(self):
        return ('https://graph.facebook.com/{facebook_id}/picture'
                '?type=large').format(facebook_id=self.facebook.uid)


@receiver(post_save, sender=User)
def first_user_is_admin(sender, instance, created,
                        raw, using, update_fields, **kwargs):
    # is this user being created, and is it the first (i.e., the only) user?
    if created and sender.objects.count() == 1:
        # give them full access
        instance.is_superuser = True
        instance.is_staff = True
        instance.is_active = True
        instance.save()
        # tell the managers what just happened, via email
        mail_managers('New superuser now has full site access.',
                      'User "{username}" is the first user to sign up, and '
                      'has been automatically granted superuser '
                      'access.'.format(username=instance.username))
