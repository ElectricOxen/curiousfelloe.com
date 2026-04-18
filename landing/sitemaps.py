from eo_site_framework.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap({'landing:home': 1.0}),
}
