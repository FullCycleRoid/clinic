from django.shortcuts import render


def main_profile_view(request):
    return render(request, 'personal_area/index.html')
