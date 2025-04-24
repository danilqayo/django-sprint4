from django.contrib import admin

from blog.models import Category, Comment, Location, Post

admin.site.empty_value_display = "Не задано"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "slug", "is_published", "created_at")

    list_editable = ("is_published",)

    search_fields = ("title",)
    list_display_links = ("title",)
    list_filter = (
        "is_published",
        "slug",
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "text",
        "pub_date",
        "is_published",
        "created_at",
        "author",
        "location",
        "category",
    )

    list_editable = ("is_published",)

    search_fields = ("title",)
    list_display_links = ("title",)
    list_filter = (
        "is_published",
        "category",
        "pub_date",
        "created_at",
        "author",
        "location",
    )
