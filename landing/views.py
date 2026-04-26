from django.shortcuts import render

from landing.models import Section


def home(request):
    """Landing page with database-driven sections."""
    sections_qs = Section.objects.filter(is_hidden=False)
    sections = {s.slug: s for s in sections_qs}
    return render(request, 'landing/home.html', {'sections': sections})
