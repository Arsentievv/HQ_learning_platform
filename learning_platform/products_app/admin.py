from django.contrib import admin
from .models import Lesson, LessonStatus, Product

admin.site.register(Lesson)
admin.site.register(LessonStatus)
admin.site.register(Product)
