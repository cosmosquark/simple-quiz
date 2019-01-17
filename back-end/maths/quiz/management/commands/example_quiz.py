from django.core.management.base import BaseCommand, CommandError
from quiz.models import Quiz, Question, Choice
from quiz.management.sample_data.example_data import example_data, \
                example_questions, example_choices

class Command(BaseCommand):
    help = "initialize the database with an example Quiz questions and answers"

    def handle(self, *args, **options):
        qz = Quiz.objects.create(**example_data)
        for i in range(0, len(example_questions)):
            ques = Question.objects.create(**example_questions[i])
            ques.quiz.add(qz)
            for j in range(0, len(example_choices[i])):
                choi = Choice.objects.create(question=ques,
                                            **example_choices[i][j])
