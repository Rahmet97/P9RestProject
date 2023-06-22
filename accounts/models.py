from django.contrib.auth.models import AbstractUser
from django.db import models


class UserData(AbstractUser):
    phone_number = models.CharField(max_length=13)
