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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.templatetags.static import static as static_asset
from django.views.generic.base import RedirectView

from apps.landing.views import LandingView

# some light admin customization
admin.site.site_title = "{{ project_name }}"

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
    url(r'^auth/login/$', auth_views.login, name='login'),
    url(r'^auth/logout/$', auth_views.logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)