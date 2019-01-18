from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import ugettext as _


class Quiz(models.Model):
    """
    A Quiz associated with questions
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
    A Question associated with multiple choices
    """
    quiz = models.ManyToManyField(Quiz,
                                  verbose_name=_("Quiz"),
                                  blank=True)
    question_text = models.CharField(max_length=200,
                                     help_text=_("The question text."),)
    position = models.IntegerField("position",
                                   help_text=_("Where is the question "
                                               "in the quiz"),)

    def __str__(self):
        return self.question_text

    def check_if_correct(self, guess):
        """
        Check if the choices provided correspond with a correct answer
        """
        # assume correct initially
        correct = True
        answers = Choice.objects.filter(id__in=guess, question=self)

        # if no answers for this question
        if len(answers) == 0:
            correct = False
            return correct

        # i.e if one is wrong, then question is wrong.
        for answer in answers:
            if answer.is_correct is False:
                correct = False
                break
        return correct

    def get_answers(self):
        return self.order_answers(Choice.objects.filter(question=self))


class Choice(models.Model):
    """
    A choice is associated with a question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name="choices")
    choice_text = models.CharField(max_length=200,
                                   help_text=_("The answer text."),)
    position = models.IntegerField("position",
                                   help_text=_("Where is the answer located "
                                               "in the question"),)
    is_correct = models.BooleanField(blank=False, default=False)

    def __str__(self):
        return self.question.question_text + ": " + self.choice_text

    class Meta:
        unique_together = [
            # no duplicated position per question
            ("question", "position")
        ]
        ordering = ("position",)
