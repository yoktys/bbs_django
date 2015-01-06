# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Forum(models.Model):

    title = models.CharField('分かりにくい場合はここに説明を入れる', max_length=60)

    def __unicode__(self):
        """
        オブジェクトを文字列に表現する際に使われる。
        Django の標準は __unicode__ だが、python 3.x からはデフォルトで unicode 対応しているので  __str__ になる。
        """
        return self.title

    def num_posts(self):
        """
        紐付いている Post の件数を返す。
        """
        return sum([t.num_posts() for t in self.thread_set.all()])

    def last_post(self):
        """
        最新 Post を返す。
        """
        # TODO N + 1 になっている。修正が必要。
        if self.thread_set.count():
            last = None
            for t in self.thread_set.all():
                l = t.last_post()
                if l:
                    if not last or l.created > last.created:
                        last = l
            return last

class Thread(models.Model):

    title = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    forum = models.ForeignKey(Forum)

    class Meta(object):
        ordering = ['-created']

    def __unicode__(self):
        return unicode(self.creator) + " - " + self.title

    def num_posts(self):
        """
        紐付いている Post の件数を返す。
        """
        return self.post_set.count()

    def num_replies(self):
        """
        返事数を返す。

        * 最初の Post 以外が返事数となる。
        * なので Thread に紐付いている Post の総数 - 1 で求められる。
        """
        return self.post_set.count() - 1

    def last_post(self):
        """
        最後に投稿された Post を返す。
        """
        if self.post_set.count():
            return self.post_set.order_by("created")[0]

class Post(models.Model):

    title = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    thread = models.ForeignKey(Thread)
    body = models.TextField(max_length=10000)

    def __unicode__(self):
        return u"%s - %s - %s" % (self.creator, self.thread, self.title)

    def short(self):
        """
        日付
        """
        return u"%s - %s\n%s" % (self.creator, self.title, self.created.strftime("%b %d, %I:%M %p"))
    short.allow_tags = True

    def profile_data(self):
        p = self.creator.userprofile_set.all()[0]
        # TODO avatar の消し忘れ。
        #      特に影響はなさそうなのでとりあえずは修正しない。
        return p.posts, p.avatar

class UserProfile(models.Model):

    posts = models.IntegerField(default=0)
    user = models.ForeignKey(User, unique=True)

    def __unicode__(self):
        return unicode(self.user)

def create_user_profile(sender, **kwargs):
    """
    ユーザ作成後、UserProfile を作成する。
    """
    u = kwargs["instance"]
    if not UserProfile.objects.filter(user=u):
        UserProfile(user=u).save()

post_save.connect(create_user_profile, sender=User)
