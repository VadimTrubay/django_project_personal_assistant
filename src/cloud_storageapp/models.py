from django.db import models

class MyModel(models.Model):
    my_file = models.FileField(upload_to='uploads/')