from django.forms import ModelForm, CharField, TextInput, Textarea, Form
from . import models


class TagForm(ModelForm):
    name = CharField(required=True)

    class Meta:
        model = models.Tag
        fields = ['name']


class NoteForm(ModelForm):
    title = CharField(required=True)
    description = CharField(required=True)

    class Meta:
        model = models.Note
        fields = ['title', 'description']
        exclude = ['tags']
