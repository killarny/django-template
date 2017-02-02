from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username',),
        }),
        (_('Personal info'), {
            'fields': (('first_name', 'last_name'), 'email'),
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'user_permissions'),
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined'),
        }),
    )
    list_display = ('name_admin', 'username', 'email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    filter_horizontal = ('user_permissions',)

    def name_admin(self, instance):
        return mark_safe('<img src="{img}" height="12" />&nbsp;{name}'.format(
            img=instance.image_url,
            name=instance.get_full_name(),
        ))
    name_admin.short_description = u'name'
