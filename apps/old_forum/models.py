# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Forum(models.Model):
    """
    フォーラムを保持するモデル。
    フォーラムは一般公開で誰からでも閲覧ができる。

    関連モデル
    ========

    * apps.forum.models.Thread
    """
    title = models.CharField('フォーラムタイトル', max_length=60, blank=False, null=False)

    def __unicode__(self):
        """
        models.Model の __unicode__ をオーバライドし、Forum モデルのコンソール表示を切り替える。
        __str__ ではないのは Django の標準が __unicode__ ベースに作成されているため。
        主に manage.py shell などのデバッグ時に使われる。
        """
        return self.title

    def num_posts(self):
        return sum([t.num_posts() for t in self.thread_set.all()])

    def last_post(self):
        if self.thread_set.count():
            last = None
            for t in self.thread_set.all():
                l = t.last_post()
                if l:
                    if not last: last = l
                    elif l.created > last.created: last = l
            return last

class Thread(models.Model):
    """
    フォーラム以下にぶら下がっているスレッドを保持するモデル。

    関連モデル
    ========

    * apps.forum.models.Forum
    * apps.forum.models.User
    """
    title = models.CharField('スレッドタイトル', max_length=60, blank=False, null=False)
    # Django 1.4 からの新機能 auto_now_add を使うと DateTimeField の初期化に便利
    user_id = models.ForeignKey(User, blank=True, null=True)
    forum_id = models.ForeignKey(Forum, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.creator) + " - " + self.title

    def num_posts(self):
        return self.post_set.count()

    def num_replies(self):
        return self.post_set.count() - 1

    def last_post(self):
        if self.post_set.count():
            return self.post_set.order_by("created")[0]


class Post(models.Model):
    """
    TODO 一般公開対象になっているが、プライベート機能の追加には対応していない。
         プライベート機能は 2014/1/31 公開予定

    関連モデル
    =========

    * apps.forum.models.User
    * apps.forum.models.Thread

    """
    title = models.CharField(max_length=60, blank=False, null=False)
    body = models.TextField('本文', max_length=10000, blank=False, null=False)
    user_id = models.ForeignKey(User, blank=True, null=True)
    thread_id = models.ForeignKey(Thread, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s - %s - %s" % (self.creator, self.thread, self.title)

    def short(self):
        return u"%s - %s\n%s" % (self.creator, self.title, self.created.strftime("%b %d, %I:%M %p"))

    short.allow_tags = True
