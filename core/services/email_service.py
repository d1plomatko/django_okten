import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from core.services.jwt_service import ActivateToken, JWTService, ResetPasswordToken


class EmailService:

    @staticmethod
    def __send_email(to: str, template_name: str, context: dict, subject=''):
        template = get_template(template_name)
        html_context = template.render(context)
        msg = EmailMultiAlternatives(subject, from_email=os.environ.get('EMAIL_HOST_USER'), to=[to])
        msg.attach_alternative(html_context, 'text/html')
        msg.send()

    @classmethod
    def register_email(cls, user,):
        token = JWTService.create_token(user, ActivateToken)
        url = f'http://localhost:3000/activate/{token}'
        cls.__send_email(user.email, 'register.html', {"name": user.profile.name, "url": url}, 'Register')

    @classmethod
    def reset_password_email(cls, user):
        token = JWTService.create_token(user, ResetPasswordToken)
        url = f'http://localhost:3000/reset_password/{token}'
        cls.__send_email(user.email, 'reset_password.html', {"name": user.profile.name, "url": url}, 'Reset Password')

