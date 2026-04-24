from django.db import models

from eo_site_framework.models import BaseMenu, BaseMenuItem, BaseSection


class Section(BaseSection):
	class Meta(BaseSection.Meta):
		pass


class Menu(BaseMenu):
	class Meta(BaseMenu.Meta):
		pass


class MenuItem(BaseMenuItem):
	menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="items")

	class Meta(BaseMenuItem.Meta):
		pass
