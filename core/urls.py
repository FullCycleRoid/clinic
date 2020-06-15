from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

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

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_change/', views.UserPasswordChangeView.as_view(), name='password_change'),

    path('password_reset/', views.EmailPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.EmailPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
]