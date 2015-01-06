# -*- coding: utf-8 -*-

from django.test import TestCase
from apps.forum.forms import PostForm

class TestPostForm(TestCase):

    def setUp(self):
        post_data = {
            'title': u'テストタイトル',
            'body': u'確認用本文',
        }
        self.form = PostForm(post_data)

    def test_is_valid(self):
        assert self.form.is_valid()

    def test_is_vailid_with_blank(self):
        self.assertFalse(PostForm().is_valid())
