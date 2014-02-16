# -*- coding: utf-8 -*-
from .models import is_pattern, Atlas, Pattern
from .sitemaps import PatternSitemap

__version_info__ = '0.2.1'
__version__ = '0.2.1'
version = '0.2.1'

__all__ = ['is_pattern', 'Atlas', 'Pattern', 'version', '__version__',
           '__version_info__', 'PatternSitemap']

urlconf = ('patternatlas.urls', 'patternatlas', 'patternatlas')
