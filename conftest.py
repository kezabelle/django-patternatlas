# -*- coding: utf-8 -*-
from __future__ import absolute_import
import django
from django.conf import settings
import os


def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests_settings")
    if settings.configured and hasattr(django, 'setup'):
        django.setup()
