from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def patient_profile_view(request):
    return render(request, 'personal_area/patient/index.html')


@login_required
def doctor_profile_view(request):
    return render(request, 'personal_area/doctor/index.html')
