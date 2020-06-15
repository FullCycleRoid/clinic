from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView
from .forms import LoginForm, RegistrationForm, PatientForm, DoctorSignUpRequestForm
from .models import CustomUser, Patient
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


"""исследовать логин вью вдоль и поперек"""
# 1 login function view
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
                return render(request, 'personal_area/index.html')

            return render(request, 'registration/signin.html', {'form': form})
        else:
            form = LoginForm()
            return render(request, 'registration/signin.html', {'form': form})
    form = LoginForm()
    return render(request, 'registration/signin.html', {'form': form})


# 2 login classBase view
# 3 ajax view
# 4 rest function view
# 5 rest class base view
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


def signout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("core:index")


class ProfileView(SuccessMessageMixin, UpdateView):
    form_class = PatientForm
    model = Patient
    template_name = 'profile/profile.html'
    success_url = '/profile/'
    success_message = 'Профиль успешно сохранен'
    error_message = 'Что то пошло не так'

    def get_object(self, queryset=None):
        return self.request.user.patient

    def get_context_data(self, **kwargs):
        instance = get_object_or_404(Patient, user=self.request.user)
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['form_class'] = self.form_class(self.request.POST, self.request.FILES, instance=instance)
        return context


# @login_required
# def profile_view(request):
#     instance = get_object_or_404(Patient, user=request.user)
#
#     if request.method == 'POST':
#         form = PatientForm(request.POST, instance=instance)
#
#         if form.is_valid():
#             profile = form.save(commit=False)
#             profile.save()
#             messages.success(request, 'Данные успешно добавлены')
#             return render(request, 'profile/profile.html', {'form': form})
#         else:
#             form.errors.as_data()
#             messages.error(request, 'Some fields was fill wrong')
#             form = PatientForm(initial=form.cleaned_data, instance=instance)
#             return render(request, 'profile/profile.html', {'form': form})
#     else:
#         user = CustomUser.objects.get(pk=request.user.pk)
#         print(user)
#         initial = Patient.objects.get(user=user)
#         print(initial.name)
#         data = {
#             'name': initial.name,
#             'surname': initial.surname,
#             'third_name': initial.third_name,
#             'birth_date': initial.birth_date,
#             'address': initial.address,
#             'mobile_phone': initial.mobile_phone,
#             'diagnose': initial.diagnose
#         }
#         form = PatientForm(initial=data, instance=instance)
#         return render(request, 'profile/profile.html', {'form': form})


# отображение запроса на регистрацию врача. Запрос должен отправляться на почту админу. Админ в ответ отправляет
# на почту ссылку на форму регистрации врача
# 1. первый этап. форма регистрации врача. С отправлением на почту админу письма с запросом и выведением страницы
# "Менеджер скоро свяжется с вами"
# 2. Второй этап страница регистрации Врача отправляется ссылкой на почту коткретному человеку
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
            return render(request, 'registration/doctor.html', {'form': form})

    else:
        form = DoctorSignUpRequestForm()
        return render(request, 'registration/doctor.html', {'form': form})


# Страница регистрация врача посылается ссылкой на почту.
# Как это сделать из админки?
# Админ должен м иметь возможность после звонка посылать на почту потенциальному врачу ссылку на форму регистрации.
# Нужно ли это вообще?
#
# Вариант 1
# Отдельная форма регистрации врача и дольнейшая обработка зарегистрированных аккаунтов обзвоном
#
# Вариант 2
# Сначала форма заяки (телефон, мыло) => звонок => сслыка на почту из админки => форма регистрации врача
#
def doctor_signup(request):
    pass


def index_or_personal_area(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('personal_area:index'))
    else:
        return HttpResponseRedirect(reverse('core:index'))


class UserPasswordChangeView(PasswordChangeView):
      success_url = 'done/'


class EmailPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('core:password_reset_done')
    email_template_name = 'registration/password_reset_email.html'


class EmailPasswordResetDoneView(PasswordResetDoneView):
    success_url = reverse_lazy('core:password_reset_complete')
