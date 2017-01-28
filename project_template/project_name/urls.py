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
from django.utils.safestring import mark_safe
from django.views.generic.base import RedirectView

# some light admin customization
admin.site.site_title = admin.site.index_title = "{{ project_name }} admin area"
admin.site.site_header = mark_safe('<img src="{img}" alt="{alt}"/>'.format(
    img=settings.STATIC_URL + 'admin/img/logo-140x60.png',
    alt=admin.site.site_title,
))


urlpatterns = [
    # standard expected resources
    url(r'^favicon.ico$', RedirectView.as_view(
        url=settings.STATIC_URL + 'favicon.ico')),
    url(r'^robots.txt$', RedirectView.as_view(
        url=settings.STATIC_URL + 'robots.txt')),

    # admin
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)