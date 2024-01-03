import re

from django import forms


class FileUploadForm(forms.Form):
    file = forms.FileField()

    folder = forms.CharField(max_length=30, required=False)

    def clean_custom_folder(self):
        custom_folder = self.cleaned_data['custom_folder']
        if not re.match(r'^[-_.A-Za-z0-9()]+(/[-_.A-Za-z0-9()]+)*$', custom_folder):
            raise forms.ValidationError(
                "Invalid folder name. Please use alphanumeric characters, hyphens, underscores, dots, and parentheses.")
        return custom_folder


