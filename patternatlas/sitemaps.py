from datetime import datetime
from django.contrib.sitemaps import Sitemap
from .models import Atlas

class PatternSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.1

    def items(self):
        return [x for x in Atlas()]
