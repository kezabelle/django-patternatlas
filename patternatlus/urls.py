from django.conf.urls import patterns, url
from .views import root, app, pattern

urlpatterns = patterns('',
                       url(regex=r'^$',
                           view=root,
                           name="index"),
                       url(regex=r'^(?P<app_label>.+)/(?P<pattern>.+)/',
                           view=pattern,
                           name="pattern"),
                       url(regex=r'^(?P<app_label>.+)/$',
                           view=app,
                           name="app"))
