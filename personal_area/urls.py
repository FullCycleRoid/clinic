from django.urls import path

from personal_area import views

app_name = 'personal_area'

urlpatterns = [
    path('doc/', views.doctor_profile_view, name='doctor_index'),
    path('patient/', views.patient_profile_view, name='patient_index'),

]