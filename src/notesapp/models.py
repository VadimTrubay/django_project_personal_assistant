from django.db import models
from usersapp.models import CustomUser


class Tag(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False)


class Note(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
