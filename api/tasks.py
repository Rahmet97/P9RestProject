import random

from celery import shared_task
from django.core.mail import send_mail
import os

from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()


@shared_task
def send_email(to_email, message, subject='Test subject', from_email='muhammadbilol550@gmail.com'):
    print(to_email)
    send_mail(
        subject,
        message,
        from_email,
        [to_email],
        fail_silently=True
    )
    return 'Done'


@shared_task
def send_sms(phone_number):
    account_sid = os.getenv('ACCOUNT_SID')
    auth_token = os.getenv('AUTH_TOKEN')
    print(f'account_sid = {account_sid}')
    print(f'auth_token = {auth_token}')
    client = Client(account_sid, auth_token)
    pin = random.randrange(1000, 9999)
    phone_number = '+998' + phone_number
    message = client.messages.create(
      body=f"Sizning tasdiqlash kodingiz: {pin}",
      from_="+13156233499",
      to=phone_number
    )
    return message.sid
