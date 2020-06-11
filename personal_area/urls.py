from django.urls import path

from personal_area import views

app_name = 'personal_area'

urlpatterns = [
    path('main/', views.main_profile_view, name='index')
]