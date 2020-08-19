from django.core.mail import send_mail
from django.template.loader import render_to_string
from clinic2.settings import ALLOWED_HOSTS, DEFAULT_TO_EMAIL
import email.header


def send_signup_request(recipient_email, phone_number):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'

    print(host)
    context = {'email': recipient_email, 'phone_number': phone_number}

    body_text = render_to_string('service_pages/mail/doctor_signup_body.txt', context)
    subject = 'Doctor sing up request'
    send_mail(subject, body_text, DEFAULT_TO_EMAIL, [DEFAULT_TO_EMAIL,])