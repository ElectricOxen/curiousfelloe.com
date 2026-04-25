"""Custom admin site for curiousfelloe.com."""

from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User

from eo_site_framework.admin import EOAdminSite


eo_admin_site = EOAdminSite(name="admin")

eo_admin_site.register(User, UserAdmin)
eo_admin_site.register(Group, GroupAdmin)
