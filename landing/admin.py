from django.contrib import admin
from curiousfelloe.admin import eo_admin_site as admin_site

from eo_site_framework.admin import BaseMenuAdmin, BaseMenuItemInline, BaseSectionAdmin
from landing.models import Menu, MenuItem, Section


class MenuItemInline(BaseMenuItemInline):
    model = MenuItem


class MenuAdmin(BaseMenuAdmin):
    inlines = [MenuItemInline]


admin_site.register(Menu, MenuAdmin)
admin_site.register(Section, BaseSectionAdmin)
