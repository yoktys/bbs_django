# -*- coding: utf-8 -*-

from django.core.context_processors import csrf

# Pagination の過去例
# ListView を使わなかった場合はこのようなコードを書かないと行けない
#
# def make_paginator(request, items, num_items):
#     paginator = Paginator(items, num_items)
#     try: page = int(request.GET.get("page", '1'))
#     except ValueError: page = 1

#     try:
#         items = paginator.page(page)
#     except (InvalidPage, EmptyPage):
#         items = paginator.page(paginator.num_pages)
#     return items

def add_csrf(request, **kwargs):
    response_params = dict(user=request.user, **kwargs)
    response_params.update(csrf(request))
    return response_params
