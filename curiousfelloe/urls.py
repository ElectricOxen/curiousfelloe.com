"""
URL configuration for curiousfelloe project.
"""
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from curiousfelloe.admin import eo_admin_site
from eo_site_framework.views.errors import page_not_found, page_forbidden
from eo_site_framework.views.health import HealthCheckView
from landing.sitemaps import sitemaps

handler403 = page_forbidden
handler404 = page_not_found

urlpatterns = [
    path('admin/', eo_admin_site.urls, name='admin'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('health/', HealthCheckView.as_view(), name='health'),
    path('', include('landing.urls', namespace='landing')),
]
