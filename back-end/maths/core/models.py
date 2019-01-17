from django.db import models
from django.conf import settings
from django.core.validators import validate_comma_separated_integer_list
from django.utils.translation import ugettext as _
from quiz.models import Quiz, Choice

class Sitting(models.Model):
    """
    Used to store the progress of logged in users sitting a quiz.
    Replaces the session system used by anon users.
    Question_order is a list of integer pks of all the questions in the
    quiz, in order.
    Question_list is a list of integers which represent id's of
    the unanswered questions in csv format.
    Incorrect_questions is a list in the same format.
    Sitting deleted when quiz finished unless quiz.exam_paper is true.
    User_answers is a json object in which the question PK is stored
    with the answer the user gave.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                verbose_name=_("User"),
                                on_delete=models.CASCADE)

    quiz = models.ForeignKey(Quiz, verbose_name=_("Quiz"),
                                on_delete=models.CASCADE)

    correct_questions_ids = models.CharField(
                            validators=[validate_comma_separated_integer_list],
                            max_length=1024)

    score = models.IntegerField(blank=True, default=0)

    user_choices = models.ManyToManyField(Choice,
                                  verbose_name=_("Choices"),
                                  blank=True)

    def __str__(self):
        return self.user.username + ": " + self.quiz.title

    @property
    def get_score(self):
        return self.score

    @property
    def get_percent_correct(self):
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
        if self.check_if_passed:
            return self.quiz.success_text
        else:
            return self.quiz.fail_text


    @property
    def get_max_score(self):
        return len(self._question_ids())


    class Meta:
        unique_together = [
            # one user takes one quiz
            ("user", "quiz"),
        ]
