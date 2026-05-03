from django.contrib import admin
from curiousfelloe.admin import eo_admin_site as admin_site

from eo_site_framework.admin import BaseSectionAdmin
from eo_site_framework.apps.site_structure.models import Menu, MenuItem, Section
from eo_site_framework.apps.site_structure.admin import MenuItemInline, MenuAdmin


admin_site.register(Menu, MenuAdmin)
admin_site.register(Section, BaseSectionAdmin)
