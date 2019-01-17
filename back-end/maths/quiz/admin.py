from django.contrib import admin

# Register your models here.
from quiz.models import Quiz, Question, Choice

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
