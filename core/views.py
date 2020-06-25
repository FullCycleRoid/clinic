from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView
from .forms import LoginForm, RegistrationForm, DoctorSignUpRequestForm, DoctorSignUpForm, BioForm
from .models import CustomUser, Doctor
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


class IndexView(TemplateView):
    template_name = 'index.html'


def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST or None)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(email, password)
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('core:personal_area'))

            return render(request, 'registration/signin.html', {'form': form})
        else:
            form = LoginForm()
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
            print(form.cleaned_data)
            CustomUser.objects.create_user(email=form.cleaned_data['email'],
                                           password=form.cleaned_data['password'],
                                           user_type=form.cleaned_data['user_type'])
            return HttpResponseRedirect(reverse('core:sign_in'))

    else:
        form = DoctorSignUpForm()
        return render(request, 'registration/doctor_signup.html', {'form': form})


def signout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("core:index")


# class DoctorProfileView(SuccessMessageMixin, UpdateView):
#     form_class = BioForm
#     model = Doctor
#     template_name = 'profile/profile.html'
#     success_url = '/profile/'
#     success_message = 'Профиль успешно сохранен'
#     error_message = 'Что то пошло не так'
#
#     def get_object(self, queryset=None):
#         return self.request.user.doctor
#
#     def get_context_data(self, **kwargs):
#         instance = get_object_or_404(Doctor, user=self.request.user)
#         context = super(DoctorProfileView, self).get_context_data(**kwargs)
#         print(self.form_class.base_fields)
#         context['form_class'] = self.form_class(self.request.POST, self.request.FILES, instance=instance)
#         return context

def doctor_profile_template_view(request):
    return render(request, 'personal_area/doctor/profile/profile.html')


@login_required()
def doctor_profile_bio_view(request):
    if request.method == 'POST':
        form = BioForm(request.POST, user=request.user)
        form.user = request.user
        print(form)
        print(form.data)
        print(form.fields)
        if form.is_valid():
            form.user = request.user
            messages.success(request, 'Ннармально все, сохранено')
            form.save()
            return render(request, 'profile/profile_bio.html', {'form': form})
    else:
        form = BioForm()
        return render(request, 'profile/profile_bio.html', {'form': form})


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


def index_or_personal_area(request):
    if request.user.is_authenticated:
        print('user type', request.user.user_type)
        if request.user.user_type == 'patient':
            return HttpResponseRedirect(reverse('personal_area:patient_index'))
        if request.user.user_type == 'doctor':
            return HttpResponseRedirect(reverse('personal_area:doctor_index'))
    else:
        return HttpResponseRedirect(reverse('core:index'))


class UserPasswordChangeView(PasswordChangeView):
    success_url = 'done/'


class EmailPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('core:password_reset_done')
    email_template_name = 'registration/password_reset_email.html'


class EmailPasswordResetDoneView(PasswordResetDoneView):
    success_url = reverse_lazy('core:password_reset_complete')
