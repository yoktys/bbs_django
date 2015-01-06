# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from apps.forum.models import Forum, Thread
from apps.forum.utils import add_csrf, make_paginator

def forum_list(request):
    """
    フォーラムのリストを表示する。
    """
    forums = Forum.objects.all()
    context = {
        'forums': forums,
        'user': request.user,
    }
    return render(request, "forum/forum_list_all.html", context)

def thread_list(request, pk):
    """
    Listing of threads in a forum.
    """
    threads = Thread.objects.filter(forum=pk).order_by("-created")
    threads = make_paginator(request, threads, 20)
    return render_to_response("forum/forum.html", add_csrf(request, threads=threads, pk=pk))
