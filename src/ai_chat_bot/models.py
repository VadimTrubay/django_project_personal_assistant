from django.db import models


# Create your models here.
class TelegramUsers(models.Model):
    custom_user_id = models.CharField(max_length=100)
    telegram_user_id = models.CharField(max_length=100, unique=True)
