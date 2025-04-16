from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

app_name = "blog"

urlpatterns = [
    path("posts/<int:pk>/", views.post_detail, name="post_detail"),
    path("posts/<int:pk>/edit/", views.PostUpdateView.as_view(), name="edit_post"),
    path(
        "posts/<int:pk>/delete/",
        views.delete_post,
        name="delete_post",
    ),
    path(
        "posts/<int:pk>/comment/",
        views.add_comment,
        name="add_comment",
    ),
    path(
        "posts/<int:pk>/delete_comment/<int:comment_pk>/",
        views.delete_comment,
        name="delete_comment",
    ),
    path(
        "posts/<int:pk>/edit_comment/<int:comment_pk>/",
        views.edit_comment,
        name="edit_comment",
    ),
    path("posts/create/", views.create_post, name="create_post"),
    path("category/<slug:category_slug>/", views.category_posts, name="category_posts"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/<str:username>/", views.user_profile, name="profile"),
    path("", views.index, name="index"),
]
