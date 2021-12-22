from django.conf import settings
from django.core.mail import send_mail
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
import pyotp
from rest_framework import status
from rest_framework.exceptions import APIException

''' 
    Initiate TOTP
    By changing the "interval" value affects the duration of OTP(one-time password).
    Example: (1 minute = 60s) If "interval" is set to 120, the duration of OTP is 2 minutes.
    By default, the OTP duration is set to 10 minutes(600s).
'''
totp = pyotp.TOTP(pyotp.random_base32(), digits=6, interval=600)


class UserEmailUtility:

    def __init__(self):
        self.activation_code = ""

    def send_activation_code(self, email_address):
        subject = "Important email: Activate your account!"
        # context_data = {"verification_code": code}
        sender_email_address = settings.EMAIL_HOST_USER

        # text_body = render_to_string(email_template_name, context_data)
        # html_body = ""
        # from_email = ""
        # email_message = EmailMultiAlternatives(subject, text_body, from_email, [to_email])
        # html_email = render_to_string(html_email_template_name, context)
        # email_message.attach_alternative(html_email, 'templates/send_activation_code.html')
        # email_message.send()

        send_mail(
            subject,
            f'Please, use the following activation code to activate your account. '
            f'\nThe activation code is valid for 10 minutes.'
            f'\nActivation code: {self.activation_code}',
            sender_email_address,
            [email_address],
            fail_silently=False,
        )

    def verify_code(self, otp):
        if otp == "":
            return False
        if otp is None:
            return False
        if not totp.verify(otp):
            raise InvalidActivationCodeException()
        return True

    def generate_activation_code(self):
        self.activation_code = totp.now()

    def get_activation_code(self):
        return self.activation_code


class InvalidActivationCodeException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "The activation code is invalid or expired"
    default_code = 'error'
