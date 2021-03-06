"""{{ project_name }} URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.templatetags.static import static as static_asset
from django.views.generic.base import RedirectView

from social_django.models import Association, Nonce, UserSocialAuth

from apps.landing.views import LandingView
from apps.registration.views import login, logout

# some light admin customization
admin.site.site_title = getattr(settings, 'SITE_NAME', '{{ project_name }}')
admin.site.login = login_required(admin.site.login)
admin.site.unregister(Group)
admin.site.unregister(Association)
admin.site.unregister(Nonce)
admin.site.unregister(UserSocialAuth)

urlpatterns = [
    # standard expected resources
    url(r'^favicon.ico$',
        RedirectView.as_view(url=static_asset('favicon.ico'))),
    url(r'^robots.txt$',
        RedirectView.as_view(url=static_asset('robots.txt'))),

    # landing page
    url(r'^$', LandingView.as_view(), name='root'),

    # admin
    url(r'^admin/', admin.site.urls),

    # auth
    url(r'^auth/login/$', login, name='login'),
    url(r'^auth/logout/$', logout, name='logout'),
    url(r'^auth/social/', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)