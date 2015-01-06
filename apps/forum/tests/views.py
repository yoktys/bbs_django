# -*- coding: utf-8 -*-

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from apps.forum.models import Forum, Thread, Post

class TestForumThreadListView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("ak", "ak@abc.org", "pwd")
        self.client = Client()
        self.client.login(username="ak", password="pwd")
        self.forum = Forum.objects.create(title="forum")
        self.site = Site.objects.create(domain="test.org", name="test.org")
        self.thread = Thread.objects.create(title="thread", creator=self.user, forum=self.forum)
        self.post = Post.objects.create(title="post", body="body", creator=self.user, thread=self.thread)

    def tearDown(self):
        self.user.delete()
        self.forum.delete()
        self.site.delete()
        self.thread.delete()
        self.post.delete()

    def test_http_ok(self):
        response = self.client.get('/forum/')
        self.assertEquals(200, response.status_code)
