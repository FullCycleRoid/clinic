import re
from django import forms
from clinic2 import settings
from .models import CustomUser, Patient


def short_pass_validation(value):
    if len(value) < 6:
        raise forms.ValidationError('Password must be minimum 6 characters', code='Password short')
    return value


class LoginForm(forms.Form):
    email = forms.CharField(max_length=20, label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password', validators=[short_pass_validation, ])

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise forms.ValidationError('No such email. Please sign up.', code='Invalid')
        return email


class RegistrationMixin(forms.Form):
    email = forms.CharField(max_length=20, label='Email')

    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Confirm password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return email
        raise forms.ValidationError('User already exists')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        if password and password1 and password != password1:
            raise forms.ValidationError("Passwords didn't match")
        return password


class RegistrationForm(RegistrationMixin):
    pass


class DoctorSignUpRequestForm(forms.Form):
    email = forms.EmailField(label='Почта')
    phone_number = forms.CharField(label='Мобильный телефон',
                                   min_length=10,
                                   max_length=15,
                                   widget=forms.TextInput(attrs={'placeholder': '+7 921 321 14 28'}))

    def clean_phone_number(self):
        value = self.cleaned_data['phone_number']
        pattern = re.compile(r'(^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$)')
        result = pattern.match(value)

        if not result:
            raise forms.ValidationError('Invalid phone number', code='Invalid')
        return result.group()


class DoctorSignUpForm(RegistrationMixin):
    user_type = forms.CharField(initial='doctor', widget=forms.HiddenInput())


class PatientBioForm(forms.ModelForm):
    birth_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,
                                 widget=forms.DateTimeInput(format="%d %m %Y",
                                                            attrs={'placeholder': '01 02 1990'}))
    phone_number = forms.CharField(label='Мобильный телефон',
                                   min_length=10,
                                   max_length=15,
                                   widget=forms.TextInput(attrs={'placeholder': '+7 921 321 14 28'}))

    class Meta:
        model = Patient
        fields = ('name', 'surname', 'third_name', 'birth_date',
                  'address', 'phone_number', 'user', 'avatar')
        widgets = {'user': forms.HiddenInput}

    def clean_phone_number(self):
        value = self.cleaned_data['phone_number']
        pattern = re.compile(r'(^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$)')
        result = pattern.match(value)

        if not result:
            raise forms.ValidationError('Invalid phone number', code='Invalid')
        return result.group()


class BioForm(forms.Form):

    user            = forms.ChoiceField(widget=forms.HiddenInput())
    birth_date      = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,
                                      widget=forms.DateTimeInput(format="%d %m %Y",
                                                                 attrs={'placeholder': '01 02 1990'}))
    phone_number    = forms.CharField(label='Мобильный телефон',
                                      min_length=10,
                                      max_length=15,
                                      widget=forms.TextInput(attrs={'placeholder': '+7 921 321 14 28'}))
    name            = forms.CharField()
    surname         = forms.CharField()
    third_name      = forms.CharField()
    avatar          = forms.ImageField()

    def clean_phone_number(self):
        value = self.cleaned_data['phone_number']
        pattern = re.compile(r'(^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$)')
        result = pattern.match(value)

        if not result:
            raise forms.ValidationError('Invalid phone number', code='Invalid')
        return result.group()