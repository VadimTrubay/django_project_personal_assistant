from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    birth_date = forms.DateField(required=True,
                                 widget=forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'year-mount-day'}))
    sex = forms.ChoiceField(required=True, choices=(("male", "male"), ("female", "female")))
    status = forms.ChoiceField(required=True, choices=(
        ("family", "family"), ("friend", "friend"), ("partner", "partner"), ("colleague", "colleague"),
        ("other", "other")))

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'address', 'phone_number', 'email', 'address', 'birth_date', 'sex',
                  'status']


class SendEmailForm(forms.ModelForm):
    coppy_to = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    theme = forms.CharField(max_length=200,
                            required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))

    text = forms.CharField(max_length=2400,
                           required=True,
                           widget=forms.Textarea(attrs={'class': 'form-control'}))

    attachment = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Contact
        fields = ['coppy_to', 'theme', 'text', 'attachment']
