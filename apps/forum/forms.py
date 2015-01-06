# -*- coding: utf-8 -*-

from django.forms import ModelForm
from apps.forum.models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ["thread", "creator"]
