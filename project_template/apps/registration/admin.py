from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
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
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    filter_horizontal = ('user_permissions',)
