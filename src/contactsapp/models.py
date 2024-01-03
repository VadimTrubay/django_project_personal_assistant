from django.db import models

from django.core.validators import RegexValidator
from django.contrib.postgres.fields import ArrayField
from datetime import datetime

"""To import top-level model from any app"""
from django.contrib.auth import get_user_model


class Contact(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(blank=False, max_length=255)
    last_name = models.CharField(blank=False, max_length=255)
    address = models.CharField(max_length=255, blank=False)
    phone_regex = RegexValidator(r'^\d{4,20}$', 'only numbers, 4-20 digit')
    phone_number = models.CharField(max_length=20, validators=[phone_regex])
    email = models.EmailField(blank=False)
    birth_date = models.DateField(blank=False)
    sex = models.CharField(blank=False, max_length=50)
    status = models.CharField(blank=False, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
