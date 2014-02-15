# -*- coding: utf-8 -*-
from .models import is_pattern, Atlus, Pattern

__version_info__ = '0.1.0'
__version__ = '0.1.0'
version = '0.1.0'

__all__ = ['is_pattern', 'Atlus', 'Pattern', 'version', '__version__',
           '__version_info__']

urlconf = ('patternatlus.urls', 'patternatlus', 'patternatlus')
