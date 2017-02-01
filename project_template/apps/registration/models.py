from django.contrib.auth.base_user import AbstractBaseUser


class User(AbstractBaseUser):
    @property
    def facebook(self):
        return self.social_auth.get(provider='facebook')

    @property
    def image_url(self):
        return ('https://graph.facebook.com/{facebook_id}/picture'
                '?type=large').format(facebook_id=self.facebook.uid)