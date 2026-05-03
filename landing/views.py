from django.shortcuts import render

from eo_site_framework.apps.site_structure.models import Section


def home(request):
    sections_qs = Section.objects.filter(is_hidden=False).order_by("display_order")
    sections = {s.slug: s for s in sections_qs}
    return render(request, "landing/home.html", {"sections": sections})
