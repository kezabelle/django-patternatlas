# -*- coding: utf-8 -*-
from .models import is_pattern, Atlas, Pattern

__version_info__ = '0.1.1'
__version__ = '0.1.1'
version = '0.1.1'

__all__ = ['is_pattern', 'Atlas', 'Pattern', 'version', '__version__',
           '__version_info__']

urlconf = ('patternatlas.urls', 'patternatlas', 'patternatlas')
