from django.db import models
from django.db.models import Manager
from core.models import CustomUser


class SecondManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class PsyTest(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    is_active = models.BooleanField(default=False)
    description = models.TextField(verbose_name='Описание', )

    objects = models.Manager()
    is_active_objects = SecondManager()

    def __str__(self):
        return self.title


class Question(models.Model):
    type_of_choice = (
        ('one_answer', 'one_answer'),
        ('multi_answer', 'multi_answer'),
        ('text_answer', 'text_answer'),
    )
    question_type = models.CharField(choices=type_of_choice, null=True, max_length=15)
    title = models.CharField(max_length=500, verbose_name='Вопрос')
    test = models.ForeignKey(PsyTest, on_delete=models.CASCADE,
                             null=True, blank=True, related_name='question')

    def __str__(self):
        return self.title


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choice')
    option = models.CharField(max_length=50, verbose_name='Варианты')

    def __str__(self):
        return self.option
