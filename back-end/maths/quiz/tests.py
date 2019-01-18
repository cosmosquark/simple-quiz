from django.test import TestCase
from .models import Quiz


class QuizTestCase(TestCase):
    def setUp(self):
        Quiz.objects.create(title="Test Quiz",
                            pass_mark=60,
                            success_text="Success",
                            fail_text="Failure")

    def test_model_access(self):
        """
        Check model creation and access
        """
        title = "Test Quiz"
        quiz = Quiz.objects.get(title=title)
        self.assertEqual(quiz.title, title)
