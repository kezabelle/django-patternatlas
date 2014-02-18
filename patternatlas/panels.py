from django.utils.translation import ugettext_lazy as _
from django.conf.urls import patterns, url
from debug_toolbar.panels import Panel
from .models import Atlas
from .views import pattern

class PatternPanel(Panel):
    nav_title = _("Pattern Atlas")
    template = 'debug_toolbar/panels/patternatlas.html'
    has_content = True

    def __init__(self, *args, **kwargs):
        super(PatternPanel, self).__init__(*args, **kwargs)
        self.atlas = Atlas()

    @property
    def title(self):
        num_patterns = len(self.atlas)
        return _("Pattern Atlas (%(count)s discovered)") % {
            'count': num_patterns}

    @property
    def nav_subtitle(self):
        num_patterns = len(self.atlas)
        return _("%(count)s patterns") % {'count': num_patterns}

    def process_response(self, request, response):
        self.record_stats({
            'patterns': self.atlas,
        })

    @classmethod
    def get_urls(cls):
        return patterns('', url(r'^pattern_detail/$', pattern,
                        name='patternatlas_detail'))
