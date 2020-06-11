from django.urls import path

from psy_tests import views

app_name = 'psy_tests'

urlpatterns = [
    path('tests/', views.psy_test_index_view, name='index'),
    path('tests/<int:id>/', views.psy_test_data, name='test'),
]