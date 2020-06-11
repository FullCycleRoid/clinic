from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index_or_personal_area, name='first'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('signin/', views.login_view, name='sign_in'),
    path('signup/', views.registration_view, name='sign_up'),
    path('signout/', views.signout_view, name='sign_out'),
    path('profile/', login_required(views.ProfileView.as_view()), name='profile'),
    # Реализовать регистрацию врача
    path('doctor-signup/', views.doctor_signup, name='doctor-signup'),
    path('doctor-signup-request/', views.doctor_signup_request, name='doctor-signup-request'),
]