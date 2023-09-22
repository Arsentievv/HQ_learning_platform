from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):

    """Модель продукта"""

    title = models.CharField(max_length=50, verbose_name="название")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="владелец")
    students = models.ManyToManyField(
        User, verbose_name="студенты", related_name="products", blank=True
    )

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"

    def __str__(self):
        return self.title


class Lesson(models.Model):

    """Модель урока"""

    title = models.CharField(max_length=50, verbose_name="название")
    video_link = models.CharField(max_length=200, verbose_name="ссылка на видео")
    watch_length = models.PositiveIntegerField(verbose_name="длительность видео")
    product = models.ManyToManyField(
        Product, related_name="lesson", verbose_name="продукт"
    )

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"

    def __str__(self):
        return self.title


class LessonStatus(models.Model):
    """Модель статуса урока"""

    status_choices = [("VIEWED", "Просмотрено"), ("NOT VIEWED", "Не просмотрено")]
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="lesson_status"
    )
    start_watching = models.DateTimeField(
        blank=True, null=True, verbose_name="дата начала просмотра видео"
    )
    finish_watching = models.DateTimeField(
        blank=True, null=True, verbose_name="дата окончания просмотра видео"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="lesson_status"
    )
    status = models.CharField(
        choices=status_choices, default="NOT VIEWED", max_length=15
    )
    updated_at = models.DateTimeField(
        blank=True, null=True, verbose_name="дата обновления"
    )
    watched_seconds = models.PositiveIntegerField(
        default=0, verbose_name="просмотрено секунд"
    )

    class Meta:
        verbose_name = "статус урока"
        verbose_name_plural = "статусы уроков"

    def __str__(self):
        return f"{self.lesson.title}-{self.status}"
