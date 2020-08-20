import nested_admin
from django.contrib import admin
from .models import CustomUser, Doctor, Appointment, MyModel

# class TocChoiceInline(nested_admin.NestedStackedInline):
#     model = Choice
#     exclude = ['user', ]
#     extra = 1
#
# class TocQuestionInline(nested_admin.NestedStackedInline):
#     model = Question
#     inlines = [TocChoiceInline]
#     extra = 1
#
#
# class PsyTestAdmin(nested_admin.NestedModelAdmin):
#     list_display = ['title', ]
#     inlines = [TocQuestionInline, ]


# admin.site.register(PsyTest, PsyTestAdmin)
admin.site.register(CustomUser)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(MyModel)

