import json

from django.shortcuts import render
from .models import PsyTest


def to_dict(instance):
    data = []
    choice = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

    for q in instance.question.all():
        data.append({'question': q.title})
        question = data[len(data) - 1]
        question['answers'] = {}
        iter = 0
        for ch in q.choice.all():
            question['answers'][choice[iter]] = ch.option
            iter += 1
    return data


def psy_test_index_view(request):
    test_list = PsyTest.objects.all()

    return render(request, 'personal_area/../templates/tests/test_list.html', {'list': test_list})


def psy_test_data(request, id):
    test = PsyTest.objects.get(id=id)
    questions = to_dict(test)
    data = json.dumps(questions, sort_keys=False,
                                 indent=4,
                                 ensure_ascii=False,
                                 separators=(',', ': '),
                      )
    print(data)

    template_name = 'tests/test.html'
    context = {'test': test, 'description': test.description, 'title': test.title, 'questions': data}

    response = render(request, template_name, context)
    return response
