from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import login as auth_login, logout_then_login
from django.core.mail import mail_managers
from django.shortcuts import redirect
from django.urls import reverse


def login(request):
    # send the user to the root url if they're already logged in
    if request.user.is_authenticated:
        return redirect('root')
    response = auth_login(request)
    # we want to use the site_name from our context_processor instead
    response.context_data.pop('site_name')
    # if facebook key/secret are missing, we can't login
    if not (settings.SOCIAL_AUTH_FACEBOOK_KEY or
                settings.SOCIAL_AUTH_FACEBOOK_SECRET):
        mail_managers('Facebook settings are missing or invalid!',
                      'Someone tried to login on the website, but your '
                      'Facebook settings are not filled out. Check your '
                      'settings file and/or Docker environment!')
        messages.error(request,
                       'Unable to sign in right now. Please try again later!')
        if settings.DEBUG:
            # add some context data if the facebook key/secret are missing
            response.context_data.update({
                'facebook_error': "Facebook settings are not filled out. "
                                  "Check your settings file and/or "
                                  "Docker environment!",
            })
        else:
            return redirect('root')
    return response


def logout(request):
    return logout_then_login(login_url=reverse('root'))