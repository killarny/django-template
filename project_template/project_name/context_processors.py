from django.conf import settings


def site_name(request):
    return {'site_name': getattr(settings, 'SITE_NAME', '{{ project_name }}')}