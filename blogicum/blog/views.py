from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import UpdateView

from blog.forms import CommentPostForm, PostForm
from blog.mixins import AuthorPostAccessMixin
from blog.models import Category, Comment, Post, User
from blog.service import get_paginated_items
from core.utils import post_all_query, post_published_query


def index(request):
    """Главгая страниц."""
    page_obj = get_paginated_items(request, post_published_query())

    context = {"page_obj": page_obj}

    return render(request, "blog/index.html", context)


def post_detail(request, pk):
    """Подробное описание поста."""
    detail = get_object_or_404(post_all_query(), pk=pk)

    if request.user != detail.author:
        if not detail.is_published or timezone.now() < detail.pub_date:
            raise Http404("Пост больше не доступен")

    form = CommentPostForm()
    context = {"post": detail, "form": form, "comments": detail.comments.all()}

    return render(request, "blog/detail.html", context)


@login_required
def create_post(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("blog:profile", username=request.user.username)

    return render(request, "blog/create.html", {"form": form})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect("blog:post_detail", pk)

    form = PostForm(instance=post)

    if request.method == "POST":
        post.delete()
        return redirect("blog:index")

    return render(request, "blog/create.html", {"form": form})


class PostUpdateView(LoginRequiredMixin, AuthorPostAccessMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("blog:post_detail", kwargs={"pk": pk})


def category_posts(request, category_slug):
    """Страница публикаций в выбранной категории."""
    category = get_object_or_404(Category,
                                 is_published=True,
                                 slug=category_slug)

    page_obj = get_paginated_items(
        request, post_published_query().filter(category=category)
    )

    context = {"category": category, "page_obj": page_obj}
    return render(request, "blog/category.html", context)


def user_profile(request, username):
    profile = get_object_or_404(User, username=username)

    if request.user != profile:
        query = post_published_query()
    else:
        query = post_all_query()

    page_obj = get_paginated_items(request, query.filter(author=profile))

    context = {
        "profile": profile,
        "page_obj": page_obj,
    }
    return render(request, "blog/profile.html", context)


def edit_profile(request):
    instance = get_object_or_404(User, username=request.user)
    form = UserChangeForm(request.POST or None, instance=instance)
    context = {"form": form}
    if form.is_valid():
        form.save()
    return render(request, "blog/user.html", context)


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentPostForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect("blog:post_detail", pk=pk)


@login_required
def edit_comment(request, pk, comment_pk):
    post = get_object_or_404(Post, pk=pk)
    comment = get_object_or_404(
        klass=Comment,
        author=request.user,
        pk=comment_pk,
        post=post,
    )

    form = CommentPostForm(request.POST or None, instance=comment)

    if form.is_valid():
        form.save()
        return redirect("blog:post_detail", pk=pk)
    context = {
        "comment": comment,
        "form": form,
    }
    return render(request, "blog/comment.html", context)


@login_required
def delete_comment(request, pk, comment_pk):
    post = get_object_or_404(Post, pk=pk)
    comment = get_object_or_404(Comment, post=post, id=comment_pk)
    if request.user != comment.author:
        return redirect("blog:post_detail", pk)
    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", pk)
    return render(request, "blog/comment.html")
