from django.contrib.auth.models import AbstractUser


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