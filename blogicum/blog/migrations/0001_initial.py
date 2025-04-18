# Generated by Django 5.1.1 on 2025-03-20 15:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_published", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("title", models.CharField(max_length=256, verbose_name="Название")),
                (
                    "description",
                    models.TextField(max_length=64, unique=True, verbose_name="Слаг"),
                ),
                ("slug", models.SlugField(unique=True, verbose_name="Слаг")),
            ],
            options={
                "verbose_name": "категория",
                "verbose_name_plural": "Категории",
            },
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_published", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("name", models.CharField(max_length=256, verbose_name="Имя")),
            ],
            options={
                "verbose_name": "Обёртка",
                "verbose_name_plural": "Обёртки",
            },
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_published", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("title", models.CharField(max_length=256, verbose_name="Название")),
                ("text", models.TextField(verbose_name="Текст")),
                ("pub_date", models.DateTimeField()),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ice_creams",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Категория",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="ice_creams",
                        to="blog.category",
                        verbose_name="Категория",
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="blog.location",
                    ),
                ),
            ],
            options={
                "verbose_name": "категория",
                "verbose_name_plural": "Категории",
            },
        ),
    ]
