from django.contrib.auth import get_user_model
from django.db import models

from blog.constants import MAX_LENGHT, MAX_LENGHT_REPRESENT
from core.models import IsPubCreateAtModel

User = get_user_model()


class Category(IsPubCreateAtModel):
    title = models.CharField("Заголовок", max_length=MAX_LENGHT)
    description = models.TextField("Описание", max_length=64, unique=True)
    slug = models.SlugField(
        "Идентификатор",
        unique=True,
        help_text=(
            "Идентификатор страницы для URL; "
            "разрешены символы латиницы, цифры, дефис и подчёркивание."
        ),
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title[:MAX_LENGHT_REPRESENT]


class Location(IsPubCreateAtModel):
    name = models.CharField("Название места", max_length=MAX_LENGHT)

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return self.name[:MAX_LENGHT_REPRESENT]


class Post(IsPubCreateAtModel):
    title = models.CharField("Заголовок", max_length=MAX_LENGHT)
    text = models.TextField("Текст")
    pub_date = models.DateTimeField(
        "Дата и время публикации",
        help_text=(
            "Если установить дату и время в будущем — "
            "можно делать отложенные публикации."
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Местоположение",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
    )

    image = models.ImageField(
        verbose_name="изображение", upload_to="blog_images/", blank=True
    )

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ["-pub_date"]
        default_related_name = "posts"

    def __str__(self):
        return self.title[:MAX_LENGHT_REPRESENT]


class Comment(models.Model):

    text = models.TextField(
        verbose_name="Комментарий",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Пост",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания",
    )

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("created_at",)

    def __str__(self):
        return (
            f"Комментарий автора {self.author} к посту {self.post} "
            f"текст: {self.text[:MAX_LENGHT_REPRESENT]}"
        )
