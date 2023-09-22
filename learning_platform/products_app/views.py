from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import (
    LessonSerializer,
    ProductSerializer,
    LessonStatusSerializer,
    ProductStatisticsSerializer,
)
from .models import Lesson, Product, LessonStatus
from datetime import datetime


class AllLessonsListAPI(generics.ListAPIView):

    """Представление для получения всех уроков конкретного ученика"""

    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        queryset = Lesson.objects.filter(product__students=self.request.user)
        return queryset


class SpecificProductDataAPI(generics.RetrieveAPIView):

    """
    Представление для получения всех уроков конкретного продукта конкретного ученика
    """

    serializer_class = ProductSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        queryset = Product.objects.filter(students=self.request.user)
        return queryset


class ProductsStatisticsAPI(generics.ListAPIView):

    """Представление для получения статистики по всем продуктам"""

    serializer_class = ProductStatisticsSerializer
    queryset = Product.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]


class StartWatching(APIView):
    def post(self, request):
        """
        Метод для отслеживания начала просмотра видео.
        - Запускается при нажатии кнопки плей с фронта.
        - Принимает АЙ-ДИ студента и АЙ-ДИ урока с фронта
        - Записывает в БД дату начала просмотра урока
        """
        data = request.data
        lesson_id = data["lesson_id"]
        user_id = data["user_id"]
        start_watching_date = datetime.utcnow()
        start_watching_date = start_watching_date.strftime("%Y-%m-%d %H:%M:%S")
        student = User.objects.get(id=user_id)
        lesson = Lesson.objects.get(id=lesson_id)
        current_lesson_status = LessonStatus.objects.get_or_create(
            lesson=lesson, student=student
        )[0]
        current_lesson_status.start_watching = start_watching_date
        serializer = LessonStatusSerializer(current_lesson_status)
        current_lesson_status.save()
        return Response({"status": "start watching", "data": serializer.data})


class FinishWatching(APIView):
    def post(self, request):
        """
        Метод для отслеживания конца просмотра видео.
        - Запускается при нажатии кнопки пауза с фронта,
           отрицательной проверки на активность сессии, переключении урока.
        - Принимает АЙ-ДИ студента и АЙ-ДИ урока с фронта
        - Проверяет, если студент посмотрел больше 80% видео,
            меняет статус на VIEWED, записывает В БД дату окончания просмотра
          и количество проссмотренных секунд
          Если меньше 80% записывает в БД сколько секунд посмотрел
        - Записывает в БД дату обновления
        """

        data = request.data
        lesson_id = data["lesson_id"]
        user_id = data["user_id"]
        finish_watching_date = datetime.utcnow()
        finish_watching_date = str(finish_watching_date.strftime("%Y-%m-%d %H:%M:%S"))
        print(finish_watching_date)
        current_lesson_status = LessonStatus.objects.get(
            lesson=lesson_id, student=user_id
        )
        time_diff = datetime.strptime(
            finish_watching_date, "%Y-%m-%d %H:%M:%S"
        ) - datetime.strptime(
            str(current_lesson_status.start_watching).split("+")[0], "%Y-%m-%d %H:%M:%S"
        )
        time_diff = time_diff.seconds
        lesson = Lesson.objects.get(id=lesson_id)
        if time_diff >= lesson.watch_length * 0.8:
            current_lesson_status.status = "VIEWED"
            current_lesson_status.finish_watching = finish_watching_date
            current_lesson_status.watched_seconds += time_diff
        else:
            current_lesson_status.watched_seconds += time_diff
        current_lesson_status.updated_at = finish_watching_date
        current_lesson_status.save()
        serializer = LessonStatusSerializer(current_lesson_status)
        current_lesson_status.save()
        return Response({"status": "finish watching", "data": serializer.data})
