from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView


class LandingView(TemplateView):
    template_name = 'landing/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        links = []
        if not self.request.user.is_authenticated:
            links.append({'name': 'login', 'url': reverse('login')})
        if self.request.user.is_staff:
            links.append({'name': 'admin', 'url': reverse('admin:index')})
        context['links'] = links
        return context