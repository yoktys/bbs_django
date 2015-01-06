# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from apps.forum.models import Forum, Thread, Post

class TestForum(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser1')
        self.forum = Forum.objects.create(title=u'フォーラムタイトル')
        self.thread = Thread.objects.create(forum=self.forum, title=u'スレッドタイトル', creator=self.user)
        Post.objects.create(title=u'ポストタイトル1', creator=self.user, thread=self.thread, body= u'本文1')
        Post.objects.create(title=u'ポストタイトル2', creator=self.user, thread=self.thread, body= u'本文2')
        Post.objects.create(title=u'ポストタイトル3', creator=self.user, thread=self.thread, body= u'本文3')

    def tearDown(self):
        self.user.delete()
        Forum.objects.all().delete()
        self.thread.delete()
        Post.objects.all().delete()

    def test_create(self):
        assert Forum.objects.create(title=u'TestForum.test_create で作成したフォーラムタイトル')

    def test__unicode__(self):
        assert u'フォーラムタイトル' == unicode(self.forum)

    def test_num_posts(self):
        assert 3 == self.forum.num_posts()

    def test_last_post(self):
        expected = Post.objects.filter(thread=self.thread).latest('created')
        result = self.forum.last_post()
        self.assertEqual(expected.id, result.id)

class TestThread(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser1')
        self.forum = Forum.objects.create(title=u'フォーラムタイトル')
        self.thread = Thread.objects.create(forum=self.forum, title=u'スレッドタイトル', creator=self.user)
        Post.objects.create(title=u'ポストタイトル1', creator=self.user, thread=self.thread, body= u'本文1')
        Post.objects.create(title=u'ポストタイトル2', creator=self.user, thread=self.thread, body= u'本文2')
        Post.objects.create(title=u'ポストタイトル3', creator=self.user, thread=self.thread, body= u'本文3')
        Post.objects.create(title=u'ポストタイトル4', creator=self.user, thread=self.thread, body= u'本文4')
        Post.objects.create(title=u'ポストタイトル5', creator=self.user, thread=self.thread, body= u'本文5')

    def tearDown(self):
        self.user.delete()
        self.forum.delete()
        Thread.objects.all().delete()
        Post.objects.all().delete()

    def test_create(self):
        assert Thread.objects.create(title=u'TestThread.test_create で作成されたスレッドタイトル', forum=self.forum)

    def test_num_posts(self):
        self.assertEqual(5, self.thread.num_posts())

    def test_num_replies(self):
        self.assertEqual(4, self.thread.num_replies())

    def test_last_post(self):
        expected = Post.objects.filter(thread=self.thread).latest('created')
        result = self.thread.last_post()
        self.assertEqual(expected.id, result.id)


class TestPost(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser1')
        self.forum = Forum.objects.create(title=u'フォーラムタイトル')
        self.thread = Thread.objects.create(forum=self.forum, title=u'スレッドタイトル', creator=self.user)
        self.post = Post.objects.create(title=u'ポストタイトル', thread=self.thread, creator=self.user, body='本文')

    def tearDown(self):
        self.user.delete()
        self.forum.delete()
        Thread.objects.all().delete()
        Post.objects.all().delete()

    def test_create(self):
        assert Post.objects.create(title=u'TestPost.test_create で作成されたポストタイトル', thread=self.thread, creator=self.user, body='本文')

    def test_short(self):
        expected = u"%s - %s\n%s" % (self.post.creator, self.post.title, self.post.created.strftime("%b %d, %I:%M %p"))
        result = self.post.short()
        self.assertEqual(expected, result)

class TestUserProfile(TestCase):
    pass
