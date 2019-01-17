from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import ugettext as _

class Quiz(models.Model):
    """
    A Quiz is made up of questions
    """
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=60, blank=False)

    pass_mark = models.SmallIntegerField(
        blank=True, default=0,
        verbose_name=_("Pass Mark"),
        help_text=_("Percentage required to pass exam."),
        validators=[MaxValueValidator(100)])

    success_text = models.TextField(
        blank=True, help_text=_("Displayed if user passes."),
        verbose_name=_("Success Text"))

    fail_text = models.TextField(
        verbose_name=_("Fail Text"),
        blank=True, help_text=_("Displayed if user fails."))

    def __str__(self):
        return self.title

    def get_questions(self):
        return self.question_set.all().select_subclasses()

    @property
    def get_max_score(self):
        return self.get_questions().count()


class Question(models.Model):
    """
    A Question has multiple choices
    """
    quiz = models.ManyToManyField(Quiz,
                                  verbose_name=_("Quiz"),
                                  blank=True)
    question_text = models.CharField(max_length=200)
    position = models.IntegerField("position")

    def __str__(self):
        return self.question_text

    def check_if_correct(self, guess):
        answers = Choice.objects.filter(id=guess, question=self)
        # i.e if one is wrong, then question is wrong.
        for answer in answers:
            if answer.is_correct is False:
                return False
        return True

    def get_answers(self):
        return self.order_answers(Choice.objects.filter(question=self))


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=200)
    position = models.IntegerField("position")
    is_correct = models.BooleanField(blank=False, default=False)

    def __str__(self):
        return self.question.question_text + ": " + self.choice_text

    class Meta:
        unique_together = [
            # no duplicated position per question
            ("question", "position")
        ]
        ordering = ("position",)
