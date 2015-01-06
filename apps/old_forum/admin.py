# -*- coding: utf-8 -*-

from django.contrib import admin
from apps.forum.models import Forum, Thread, Post

class ForumAdmin(admin.ModelAdmin):
    pass

class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'forum_id', 'user_id', 'created_at', 'updated_at']
    list_filter = ['forum_id', 'user_id']

class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'user_id']
    list_display = ['title', 'thread_id', 'user_id', 'created_at', 'updated_at']

admin.site.register(Forum, ForumAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)
