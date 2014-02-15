from django_medusa.renderers import StaticSiteRenderer
from django.core.urlresolvers import reverse
from .models import Atlas


class AtlasRenderer(StaticSiteRenderer):
    def get_paths(self):
        urls = set()
        urls.add(reverse('patternatlas:index'))
        for pattern in Atlas():
            urls.add(pattern.get_absolute_url())
            urls.add(pattern.get_parent_url())
        return sorted(urls, key=len)

renderers = (AtlasRenderer,)
