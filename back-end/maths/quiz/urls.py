from django.urls import path
from .views import QuizAPI

urlpatterns = [
    path('<int:pk>/', QuizAPI.as_view()),
]
