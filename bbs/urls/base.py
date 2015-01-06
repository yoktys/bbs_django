# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.views.generic import ListView

from django.contrib import admin
admin.autodiscover()

from apps.forum.models import Forum

urlpatterns = patterns('',
    # forum
    url(r'^forum/', include('apps.forum.urls')),

    # registration
    url(r'^accounts/', include('registration.backends.default.urls')),

    # Django admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', ListView.as_view(model=Forum))
)
