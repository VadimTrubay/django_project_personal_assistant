from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CustomUserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=100,
                             required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))

    username = forms.CharField(max_length=20,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(max_length=100,
                                 required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(max_length=100,
                                required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    password1 = forms.CharField(max_length=16,
                                required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(max_length=16,
                                required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    # email = forms.EmailField(max_length=100,
    #                          required=True,
    #                          widget=forms.EmailInput(attrs={'class': 'form-control'}))

    username = forms.CharField(max_length=20,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(max_length=16,
                               required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'password']
