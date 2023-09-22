from django.urls import path
from .views import (
    AllLessonsListAPI,
    SpecificProductDataAPI,
    ProductsStatisticsAPI,
    StartWatching,
    FinishWatching,
)

urlpatterns = [
    path("all_user_lessons/", AllLessonsListAPI.as_view(), name="all_users_lessons"),
    path(
        "product/<int:pk>/", SpecificProductDataAPI.as_view(), name="specific_product"
    ),
    path("statistics/", ProductsStatisticsAPI.as_view(), name="statistics"),
    path("start_watching/", StartWatching.as_view(), name="start_watching"),
    path("finish_watching/", FinishWatching.as_view(), name="finish_watching"),
]
