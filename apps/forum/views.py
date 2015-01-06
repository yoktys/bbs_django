# -*- coding: utf-8 -*-

# import 文のボリュームが増えた場合は、上位ライブラリ順で並べる。
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response, render
from django.core.urlresolvers import reverse
from django.views.generic import View, ListView
from django.utils.decorators import method_decorator

# 特に独自ものに関しては一番したの方が分かりやすく編集しやすい。
from apps.forum.models import Forum, Thread, Post
from apps.forum.forms import PostForm
from apps.forum.utils import add_csrf

class DisableHttpGetMixIn(object):
    """
    HTTP GET を無効にする。
    """

    def get(self, *args, **kwargs):
        raise Http404

class ForumThreadListView(ListView):
    """
    Forum に紐付いている Thread のリストを表示する。
    """

    # これらは ListView で利用される決まりな変数なのでコメントがなくても分かりやすい。
    context_object_name = 'thread_list'
    template_name = 'forum/thread_list.html'
    paginate_by = 20

    def get_queryset(self):
        """
        指定された Forum.id を参照している Thread のリストを表示する。

        * Forum.id: self.args[0]
        """
        self.forum = get_object_or_404(Forum, id=self.args[0])
        thread_list = Thread.objects.filter(forum=self.forum)
        return thread_list

    def get_context_data(self, **kwargs):
        """
        コンテキストに forum_pk を追加して返す。
        forum_pk は現在のコネクションで指定された Forum.id。
        """
        context = super(ForumThreadListView, self).get_context_data(**kwargs)
        context['forum_pk'] = self.forum.id
        return context

class ThreadPostListView(ListView):
    """
    Thread に紐付いている Post のリストを表示する。
    """

    context_object_name = 'post_list'
    template_name = 'forum/post_list.html'
    paginate_by = 15

    def get_queryset(self):
        """
        指定の Thread.id を参照している Post のリストを表示する。
        """
        self.thread = get_object_or_404(Thread, id=self.args[0])
        post_list = Post.objects.filter(thread=self.thread)
        return post_list

    def get_context_data(self, **kwargs):
        """
        コンテキストに forum_pk と thread_pk を追加する。

        * forum_pk: Thread が参照している Forum.id。
        * thread_pk: 指定の Thread.id。
        """
        context = super(ThreadPostListView, self).get_context_data(**kwargs)
        context['forum_pk'] = self.thread.forum.id
        context['thread_pk'] = self.thread.id
        return context

class ProfileView(View):
    """
    ログインした現在ユーザのプロフィールを表示する。

    TODO 2099/12/12 まで修正機能追加が予定されている。
    """

    @method_decorator(login_required)
    def get(self, request, pk):
        user = request.user
        context = {
            'username': user,
            'useremail': user.email
        }
        return render(self.request, 'forum/profile.html', context)

    def post(self, request, *args, **kwargs):
        pass

class NewPostingView(View):
    """
    新しい Thread と Post の追加フォームを表示する。

    * urls 設定: (new_thread|reply)
    """

    @method_decorator(login_required)
    def get(self, request, post_type, pk):
        # url パスを見てフォームの着地点を決める。
        if post_type == "new_thread":
            form_action = reverse('create_thread_view', args=[pk])
            title = "Start New Topic"
            subject = ''
        elif post_type == "reply":
            form_action = reverse('create_post_reply_view', args=[pk])
            title = "Reply"
            subject = "Re: " + Thread.objects.get(pk=pk).title

        context = {
            'title': title,
            'subject': subject,
            'action': form_action,
        }
        return render_to_response('forum/new_posting.html', add_csrf(self.request, **context))

def increment_post_counter(request):
    """
    新しい Thread と Post の作成時に UserProfile.posts を更新する。
    """
    profile = request.user.userprofile_set.all()[0]
    profile.posts += 1
    profile.save()

class CreateThreadView(DisableHttpGetMixIn, View):
    """
    新しい Thread を作成する。NewPostingView から転送された HTTP POST を処理する。
    """

    @method_decorator(login_required)
    def post(self, request, pk):
        form = PostForm(request.POST)
        if form.is_valid():
            forum = Forum.objects.get(pk=pk)
            new_thread = Thread.objects.create(forum=forum, title=request.POST['title'], creator=request.user)
            new_post = form.save(commit=False)
            new_post.creator = request.user
            new_post.thread = new_thread
            new_post.save()
            increment_post_counter(request)
            return HttpResponseRedirect(reverse("thread_post_list_view", args=[new_thread.id]))
        return render_to_response('form/new_posting.html', {form: form})

class CreatePostReplyView(DisableHttpGetMixIn, View):
    """
    新しい Post を作成する。NewPostingView から転送された HTTP POST を処理する。
    Thread を参照するのでその pk の指定が必要。
    """

    @method_decorator(login_required)
    def post(self, request, pk):
        """
        ModelForm を使わなくても HTTP POST の処理は可能。
        以下のコードは一見短く綺麗に見えるが、validation が走らないのでデータの整合性を自前でチェックするしかない。
        """
        p = request.POST
        if p["body"]:
            thread = Thread.objects.get(pk=pk)
            post = Post.objects.create(thread=thread, title=p["title"], body=p["body"], creator=request.user)
            if post:
                increment_post_counter(request)
        return HttpResponseRedirect(reverse("thread_post_list_view", args=[pk]) + "?page=last")
