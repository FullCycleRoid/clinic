import nested_admin
from django.contrib import admin
from psy_tests.models import PsyTest, Question, Choice
from .models import CustomUser, Patient, Doctor


class TocChoiceInline(nested_admin.NestedStackedInline):
    model = Choice
    exclude = ['user', ]
    extra = 1

class TocQuestionInline(nested_admin.NestedStackedInline):
    model = Question
    inlines = [TocChoiceInline]
    extra = 1


class PsyTestAdmin(nested_admin.NestedModelAdmin):
    list_display = ['title', ]
    inlines = [TocQuestionInline, ]


admin.site.register(PsyTest, PsyTestAdmin)
admin.site.register(CustomUser)
admin.site.register(Patient)
admin.site.register(Doctor)
