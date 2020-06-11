from django import forms
from psy_tests.models import Question


class SingleQuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['title', ]
