# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, InvalidPage, EmptyPage

def make_paginator(request, items, num_items):
    """
    Create and return a paginator.
    """
    paginator = Paginator(items, num_items)
    try:
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1

    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items
