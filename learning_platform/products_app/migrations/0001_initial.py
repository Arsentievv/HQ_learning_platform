# Generated by Django 4.2.1 on 2023-09-21 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Lesson",
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
                ("title", models.CharField(max_length=50, verbose_name="название")),
                (
                    "video_link",
                    models.CharField(max_length=200, verbose_name="ссылка на видео"),
                ),
                (
                    "watch_length",
                    models.PositiveIntegerField(verbose_name="длительность видео"),
                ),
            ],
            options={
                "verbose_name": "урок",
                "verbose_name_plural": "уроки",
            },
        ),
        migrations.CreateModel(
            name="Product",
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
                ("title", models.CharField(max_length=50, verbose_name="название")),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="владелец",
                    ),
                ),
                (
                    "students",
                    models.ManyToManyField(
                        blank=True,
                        related_name="products",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="студенты",
                    ),
                ),
            ],
            options={
                "verbose_name": "продукт",
                "verbose_name_plural": "продукты",
            },
        ),
        migrations.CreateModel(
            name="LessonStatus",
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
                ("start_watching", models.DateTimeField()),
                ("finish_watching", models.DateTimeField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("VIEWED", "Просмотрено"),
                            ("NOT VIEWED", "Не просмотрено"),
                        ],
                        default="V",
                        max_length=15,
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lesson_status",
                        to="products_app.lesson",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lesson_status",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "статус урока",
                "verbose_name_plural": "статусы уроков",
            },
        ),
        migrations.AddField(
            model_name="lesson",
            name="product",
            field=models.ManyToManyField(
                related_name="lesson", to="products_app.product", verbose_name="продукт"
            ),
        ),
    ]
