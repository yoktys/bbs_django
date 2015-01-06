# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from apps.forum.views import ForumThreadListView, ThreadPostListView, NewPostingView, ProfileView, CreatePostReplyView, CreateThreadView

urlpatterns = patterns('apps.forum.views',
    url(r'^(\d+)/$', ForumThreadListView.as_view(), name='forum_thread_list_view'),
    url(r'^thread/(\d+)/$', ThreadPostListView.as_view(), name='thread_post_list_view'),
    url(r'^post/(new_thread|reply)/(\d+)/$', NewPostingView.as_view(), name='new_posting_view'),
    url(r'^reply/(\d+)/$', CreatePostReplyView.as_view(), name='create_post_reply_view'),
    url(r'^profile/(\d+)/$', ProfileView.as_view(), name='profile_view'),
    url(r'^new_thread/(\d+)/$', CreateThreadView.as_view(), name='create_thread_view'),
)
