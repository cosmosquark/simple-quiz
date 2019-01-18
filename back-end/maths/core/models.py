from django.db import models
from django.conf import settings
from django.core.validators import validate_comma_separated_integer_list
from django.utils.translation import ugettext as _
from quiz.models import Quiz, Question, Choice


class Sitting(models.Model):
    """
    The sitting model handels users progress through a quiz.
    Stores the users submitted choices and computes the answer
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=("User"),
                             help_text=_("User"),
                             on_delete=models.CASCADE)

    quiz = models.ForeignKey(Quiz, verbose_name=_("Quiz"),
                             on_delete=models.CASCADE,
                             help_text=_("The quiz the user is taking"))

    score = models.IntegerField(blank=True, default=0,
                                help_text=_("The user's quiz score."),)

    user_choices = models.ManyToManyField(Choice,
                                          verbose_name=_("Choices"),
                                          blank=True,
                                          help_text=_("The user's submitted "
                                                      "answers"),)

    def __str__(self):
        return self.user.username + ": " + self.quiz.title

    @property
    def get_score(self):
        """
        Return the total score to the user
        """
        return self.score

    @property
    def get_percent_correct(self):
        """
        Calculate a total percentage score based on the current score.
        """
        dividend = float(self.current_score)
        divisor = self.quiz.get_max_score()
        if divisor < 1:
            return 0            # prevent divide by zero error

        if dividend > divisor:
            return 100

        correct = int(round((dividend / divisor) * 100))

        if correct >= 1:
            return correct
        else:
            return 0

    @property
    def check_if_passed(self):
        return self.get_percent_correct >= self.quiz.pass_mark

    @property
    def result_message(self):
        """
        Select the result message to display from the quiz
        """
        if self.check_if_passed:
            return self.quiz.success_text
        else:
            return self.quiz.fail_text

    @property
    def get_max_score(self):
        return len(self._question_ids())

    def calculate_score(self):
        """
        Update the score from the recent submissions
        From the submitted user choices, check them against each question.
        If all choices in a question are correct, then append the score by 1.
        """
        # reset the score to 0
        self.score = 0
        questions = Question.objects.filter(quiz=self.quiz)
        for question in questions:
            correct = question.check_if_correct(self.user_choices
                                                .values_list("id"))
            if correct is True:
                self.score += 1

    class Meta:
        unique_together = [
            # one user takes one quiz
            ("user", "quiz"),
        ]
