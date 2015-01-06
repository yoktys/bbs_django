# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.forum.views',
    url(r'forum_list_all/$', 'forum_list_all'),
    url(r'(\d+)/$', 'forum'),
    url(r'thread/(\d+)/$', 'thread'),
)
