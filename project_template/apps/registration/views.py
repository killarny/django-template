from django.contrib.auth.views import login as auth_login, logout_then_login
from django.urls import reverse


def login(request):
    response = auth_login(request)
    # we want to use the site_name from our context_processor instead
    response.context_data.pop('site_name')
    return response


def logout(request):
    return logout_then_login(login_url=reverse('root'))