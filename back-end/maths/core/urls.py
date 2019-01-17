from django.urls import path
from .views import current_user, UserList, SittingAPI

urlpatterns = [
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
    path('quiz/<int:pk>/', SittingAPI.as_view()),
]
