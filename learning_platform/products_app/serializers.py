from django.contrib.auth.models import User
from rest_framework import serializers
from .models import LessonStatus, Lesson, Product


class LessonStatusSerializer(serializers.ModelSerializer):

    """Сериалайзер для модели урока"""

    class Meta:
        model = LessonStatus
        fields = ["status", "watched_seconds", "updated_at"]


class LessonSerializer(serializers.ModelSerializer):

    """Сериалайзер для модели урока с полем статуса просмотра видео"""

    lesson_status = LessonStatusSerializer(many=True)

    class Meta:
        model = Lesson
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):

    """Сериалайзер для модели продукта, с информацией по урокам"""

    lesson = LessonSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductStatisticsSerializer(serializers.ModelSerializer):

    """Сериалайзер для модели продукта, со статистикой"""

    students_amt = serializers.SerializerMethodField()
    buying_percent = serializers.SerializerMethodField()
    viewed_lessons_count = serializers.SerializerMethodField()
    total_watch_time = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_students_amt(self, obj):
        """Метод получения количества учеников продукта"""

        students_amt = obj.students.count()
        return students_amt

    def get_buying_percent(self, obj):
        """Метод получения процента покупок продукта"""

        all_users = len(User.objects.all())
        students_amt = obj.students.count()
        buying_percent = students_amt / all_users * 100
        return buying_percent

    def get_viewed_lessons_count(self, obj):
        """Метод получения количества просмотренных видео продукта"""

        product = Product.objects.get(id=obj.id)
        students_list = User.objects.filter(products=product)
        lessons_list = Lesson.objects.filter(product=product)
        total_viewed_lessons_count = 0
        for student in students_list:
            for lesson in lessons_list:
                lesson_status = LessonStatus.objects.get(student=student, lesson=lesson)
                if lesson_status.status == "VIEWED":
                    total_viewed_lessons_count += 1
        return total_viewed_lessons_count

    def get_total_watch_time(self, obj):
        """Метод получения общего времени просмотра видео продукта"""

        product = Product.objects.get(id=obj.id)
        students_list = User.objects.filter(products=product)
        lessons_list = Lesson.objects.filter(product=product)
        total_watch_time = 0
        for student in students_list:
            for lesson in lessons_list:
                lesson_status = LessonStatus.objects.get(student=student, lesson=lesson)
                total_watch_time += lesson_status.watched_seconds
        return total_watch_time
