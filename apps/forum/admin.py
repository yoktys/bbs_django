# -*- coding: utf-8 -*-

from django.contrib import admin
from apps.forum.models import Forum, Thread, Post, UserProfile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user"]

class ForumAdmin(admin.ModelAdmin):
    pass

class ThreadAdmin(admin.ModelAdmin):
    list_display = ["title", "forum", "creator", "created"]
    list_filter = ["forum", "creator"]

class PostAdmin(admin.ModelAdmin):
    search_fields = ["title", "creator"]
    list_display = ["title", "thread", "short", "creator", "created"]

admin.site.register(Forum, ForumAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(UserProfile, ProfileAdmin)
