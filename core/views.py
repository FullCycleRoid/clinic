from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView, ListView, DetailView, FormView
from .decorators import ajax_required
from .forms import LoginForm, RegistrationForm, DoctorSignUpRequestForm, DoctorSignUpForm, DoctorBioForm, \
    PatientBioForm, AppointmentForm
from .models import CustomUser, Doctor, Patient
from .utilities import send_signup_request


class ErrorMessageMixin:
    """
    Add a success message on successful form submission.
    """
    error_message = ''

    def form_valid(self, form):
        response = super().form_valid(form)
        error_message = self.get_error_message(form.cleaned_data)
        if error_message:
            messages.error(self.request, error_message)
        return response

    def get_error_message(self, cleaned_data):
        return self.error_message % cleaned_data


def index_or_personal_area(request):
    if request.user.is_authenticated:
        print('user type', request.user.user_type)
        if request.user.user_type == 'patient':
            return HttpResponseRedirect(reverse('personal_area:patient_index'))
        if request.user.user_type == 'doctor':
            return HttpResponseRedirect(reverse('personal_area:doctor_index'))
    else:
        return HttpResponseRedirect(reverse('core:index'))


class IndexView(TemplateView):
    template_name = 'index.html'


# REGISTRATION
def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('core:personal_area'))
            return render(request, 'registration/signin.html', {'form': form})
        else:
            form = LoginForm(request.POST)
            return render(request, 'registration/signin.html', {'form': form})
    form = LoginForm()
    return render(request, 'registration/signin.html', {'form': form})


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            CustomUser.objects.create_user(email=email, password=password)
            return HttpResponseRedirect(reverse('core:sign_in'))
        else:
            form = RegistrationForm(initial=form.cleaned_data)
            return render(request, 'registration/signup.html', {'form': form})
    else:
        form = RegistrationForm()
        return render(request, 'registration/signup.html', {'form': form})


def doctor_signup(request):
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            CustomUser.objects.create_user(email=form.cleaned_data['email'],
                                           password=form.cleaned_data['password'],
                                           user_type=form.cleaned_data['user_type'])
            return HttpResponseRedirect(reverse('core:sign_in'))
        return render(request, 'registration/doctor_signup.html', {'form': form})
    else:
        form = DoctorSignUpForm()
        return render(request, 'registration/doctor_signup.html', {'form': form})


def signout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("core:index")


def doctor_signup_request(request):
    if request.method == 'POST':
        form = DoctorSignUpRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            send_signup_request(email, phone_number)
            title = 'Форма отправлена'
            body = 'Менеджер скоро свяжется с вами'
            return render(request, 'service/thanks.html', {'title': title, 'body': body})
        else:
            messages.error(request, 'Введите корректный номер телефона')
            form = DoctorSignUpRequestForm()
            return render(request, 'registration/doctor_signup.html', {'form': form})
    else:
        form = DoctorSignUpRequestForm()
        return render(request, 'registration/doctor_signup.html', {'form': form})


class UserPasswordChangeView(PasswordChangeView):
    success_url = 'done/'


class EmailPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('core:password_reset_done')
    email_template_name = 'registration/password_reset_email.html'


class EmailPasswordResetDoneView(PasswordResetDoneView):
    success_url = reverse_lazy('core:password_reset_complete')


# PROFILES INFO
class DoctorProfileView(SuccessMessageMixin, UpdateView):
    form_class = DoctorBioForm
    model = Doctor
    template_name = 'profile/profile.html'
    success_url = '/doc/profile/'
    success_message = 'Профиль успешно сохранен'
    error_message = 'Что то пошло не так'

    def get_object(self, queryset=None):
        return self.request.user.doctor

    def get_context_data(self, **kwargs):
        instance = get_object_or_404(Doctor, user=self.request.user)
        context = super(DoctorProfileView, self).get_context_data(**kwargs)
        context['form_class'] = self.form_class(self.request.POST, self.request.FILES, instance=instance)
        return context


class PatientProfileView(SuccessMessageMixin, UpdateView):
    form_class = PatientBioForm
    model = Patient
    template_name = 'profile/profile.html'
    success_url = '/patient/profile/'
    success_message = 'Профиль успешно сохранен'
    error_message = 'Что то пошло не так'

    def get_object(self, queryset=None):
        return self.request.user.patient

    def get_context_data(self, **kwargs):
        instance = get_object_or_404(Patient, user=self.request.user)
        context = super(PatientProfileView, self).get_context_data(**kwargs)
        context['form_class'] = self.form_class(self.request.POST, self.request.FILES, instance=instance)
        return context


class DoctorList(ListView):
    model = Doctor
    template_name = 'personal_area/patient/doctor_list.html'
    context_object_name = 'doctors'


class DoctorDetail(DetailView, FormView):
    model = Doctor
    form_class = AppointmentForm
    template_name = 'personal_area/patient/doctor_detail.html'
    context_object_name = 'doctor'


@login_required
@ajax_required
def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            return JsonResponse('OK')
    else:
        form = AppointmentForm()
        return render(request, 'personal_area/patient/appointment_ajax.html',
                      {'form': form})