# -*- coding: utf-8 -*-
from .models import is_pattern, Atlas, Pattern

__version_info__ = '0.2.0'
__version__ = '0.2.0'
version = '0.2.0'

__all__ = ['is_pattern', 'Atlas', 'Pattern', 'version', '__version__',
           '__version_info__']

urlconf = ('patternatlas.urls', 'patternatlas', 'patternatlas')
