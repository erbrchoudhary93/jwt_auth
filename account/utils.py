from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings


import os

class Utils:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            
            subject=data['subject'],
            body = data['body'],
            from_email=os.environ.get('EMAIL_HOST_USER'),
            to=(data['to_email'],)
            
            )
        email.send()
        
        

# # for sending mail function
# def send_mail_after_registration(email,token):
#     subject = "Verify your account"
#     message = f'Hello  !! \n Welcome to Cropto Lover ! \n  Thank you for visiting Our Website \n We have also send Conformation  Email , Please conform your email address to activate your account. \n\n Thank You \n Ziddi Engineer \n Please click on this link to verify Account \n  http://127.0.0.1:8000/account_verify/{token}'
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list =[email]
#     send_mail(subject=subject ,message=message,from_email=from_email,recipient_list=recipient_list)
    