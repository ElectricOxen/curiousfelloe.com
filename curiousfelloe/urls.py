"""
URL configuration for curiousfelloe project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from eo_site_framework.views.health import HealthCheckView
from landing.sitemaps import sitemaps

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('health/', HealthCheckView.as_view(), name='health'),
    path('', include('landing.urls', namespace='landing')),
]
