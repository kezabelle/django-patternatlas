#! /usr/bin/env python
from __future__ import unicode_literals
import os
import sys
from importd import d

HERE = os.path.realpath(os.path.dirname(__file__))
PARENT = os.path.realpath(os.path.dirname(HERE))
sys.path.append(PARENT)

d(
    SITE_ID=1,
    DEBUG=True,
    TEMPLATE_DEBUG=True,
    LANGUAGES=[
        ('en', 'English'),
    ],
    INSTALLED_APPS=[
        "django.contrib.sites",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.staticfiles",
        "django.contrib.messages",
        "django.contrib.admin",
        "django.contrib.sitemaps",
        "debug_toolbar",
        "test_app",
        "another_test_app",
        "patternatlas",
        "django_pygments",
        "django_medusa",
    ],
    MIDDLEWARE_CLASSES=[
        "django.middleware.common.CommonMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ],
    INTERNAL_IPS=[
        "127.0.0.1",
    ],
    DEBUG_TOOLBAR_PATCH_SETTINGS=False,
    DEBUG_TOOLBAR_PANELS=[
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    DEBUG_TOOLBAR_CONFIG={
        "INTERCEPT_REDIRECTS": False,
        "ENABLE_STACKTRACES": True,
        "SHOW_TEMPLATE_CONTEXT": True,
        "SQL_WARNING_THRESHOLD": 300,
    },
    TEMPLATE_CONTEXT_PROCESSORS=[
        "django.core.context_processors.media",
        "django.core.context_processors.static",
        "django.core.context_processors.request",
        "django.contrib.auth.context_processors.auth",
    ],
    SESSION_ENGINE="django.contrib.sessions.backends.file",
    STATIC_URL='/s/',
    MEDIA_URL='/m/',
    MEDUSA_RENDERER_CLASS="django_medusa.renderers.DiskStaticSiteRenderer",
    MEDUSA_DEPLOY_DIR=os.path.realpath(os.path.join(HERE, '_build')),
)

from django.conf.urls import include
import debug_toolbar
import patternatlas
from patternatlas.publishers import PatternPublisher

sitemaps = {
    'atlas': patternatlas.PatternSitemap,
}
d.urlpatterns += d.patterns('',
                            d.url(r'^debug_toolbar/',
                                  include(debug_toolbar.urls)),
                            d.url(r'^sitemap\.xml$',
                                  'django.contrib.sitemaps.views.sitemap',
                                  {'sitemaps': sitemaps}),
                            d.url(r'^api/',
                                  include(PatternPublisher.patterns())),
                            d.url(r'^', include(patternatlas.urlconf)))


if __name__ == "__main__":
    d.do("syncdb", "--noinput")
    from django.contrib.auth.models import User
    admin_user, created = User.objects.get_or_create(username="admin",
                                                     is_active=True,
                                                     is_staff=True,
                                                     is_superuser=True)
    admin_user.set_password('admin')
    admin_user.save()
    d.main()
