import datetime

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """User additional information"""
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    users = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('assistant', 'Assistant'),
    )

    user_type = models.CharField(choices=users, max_length=9, default='patient')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    name = models.CharField(max_length=20, verbose_name='Имя', blank=True, null=True)
    about = models.CharField(max_length=1000, verbose_name='О себе', blank=True, null=True)
    surname = models.CharField(max_length=20, verbose_name='Фамилия', blank=True, null=True)
    third_name = models.CharField(max_length=20, verbose_name='Отчество', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    citizenship = models.CharField(max_length=50, verbose_name='Гражданство', blank=True, null=True)
    passport = models.IntegerField(verbose_name='Паспортные данные', blank=True, null=True)
    phone_number = models.IntegerField(verbose_name='Номер телефона', blank=True, null=True)
    # https: // github.com / matthewwithanm / django - imagekit
    # в дальнейщем исползовать данный пакет работы с изображениями
    avatar = models.ImageField(upload_to='images/avatars/%Y/%m/%d/',
                               default='/static/default_img/default.png')
    city = models.CharField(max_length=50, verbose_name='Город', blank=True, null=True)
    street = models.CharField(max_length=50, verbose_name='Улица', blank=True, null=True)
    apartment = models.CharField(max_length=50, verbose_name='Квартира', blank=True, null=True)
    address = models.CharField(max_length=150, verbose_name='Полный адрес', blank=True, null=True)

    def full_address(self):
        self.address = f'{self.city}, {self.street}, {self.apartment}'
        return f'{self.city}, {self.street}, {self.apartment}'

    def save(self, *args, **kwargs):
        self.full_address()
        super().save(*args, **kwargs)

    def age(self):
        if self.birth_date:
            return int((datetime.datetime.now().date() - self.birth_date).days / 365.25)
        return 'Укажите возраст в профиле'

    def full_name(self):
        return f'{self.name} {self.surname} {self.third_name}'

    def __str__(self):
        return self.full_name()

    class Meta:
        abstract = True


class DoctorProfile(Profile):
    working_experience = models.CharField(max_length=50, verbose_name='Опыт работы', blank=True, null=True)
    appointments_per_hour = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    specialty = models.CharField(max_length=20, verbose_name='Специализация')

    class Meta:
        abstract = True


class PatientProfile(Profile):
    diagnose = models.CharField(max_length=50, verbose_name='Диагноз', blank=True, null=True)

    class Meta:
        abstract = True


class MedicalRecords(models.Model):
    pass


class Patient(PatientProfile):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient')
    user.user_type = "patient"


class Doctor(DoctorProfile):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor')
    user.user_type = "doctor"


class Appointment(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient')

    def __str__(self):
        return str(self.doctor) + " " + str(self.patient) + " - " + str(self.date)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "doctor":
            Doctor.objects.create(user=instance)
        elif instance.user_type == "patient":
            Patient.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == "doctor":
        instance.doctor.save()
    elif instance.user_type == "patient":
        instance.patient.save()


class MyModel(models.Model):
    text = models.CharField(max_length=100)