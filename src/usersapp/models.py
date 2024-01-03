from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
        ('manager', 'Manager'),
        ('developer', 'Developer'),
        ('support', 'Support'),
    )

    role = models.CharField(max_length=120, choices=ROLE_CHOICES, default='user')
    telegram_id = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f' User - {self.username} has a role:  {self.role}'
