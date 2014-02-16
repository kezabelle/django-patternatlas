from django.conf.urls import patterns, url, include
from .views import root, app, pattern
from .publishers import PatternPublisher

urlpatterns = patterns('',
                       url(regex=r'^api/',
                           view=include(PatternPublisher.patterns())),
                       url(regex=r'^$',
                           view=root,
                           name="index"),
                       url(regex=r'^(?P<app_label>.+)/(?P<pattern>.+)/',
                           view=pattern,
                           name="pattern"),
                       url(regex=r'^(?P<app_label>.+)/$',
                           view=app,
                           name="app"))
