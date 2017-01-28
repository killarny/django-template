from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView


class LandingView(TemplateView):
    template_name = 'landing/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_name'] = "{{ project_name }}"
        context['links'] = [
            {'name': 'admin', 'url': reverse('admin:index')},
        ]
        return context