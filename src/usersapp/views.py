from django.core.mail import EmailMessage

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from . import forms
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site

from .tokens import account_activation_token

from .models import CustomUser


def main(request):
    return render(request=request, template_name='usersapp/index.html', context={})


def root(request):
    return render(request=request, template_name='usersapp/main.html', context={})


def terms(request):
    return render(request=request, template_name='usersapp/terms.html', context={})


def create_user_profile(request):
    if request.user.is_authenticated:
        return redirect('usersapp:main')

    if request.method == 'POST':
        form = forms.CustomUserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            # user.save()
            form.save()
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('usersapp/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            print(message)
            to_email = form.cleaned_data.get('email')
            print(to_email)
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            print("Email Sending .....")
            email.send()
            return redirect('usersapp:login_user')

        else:
            print("Form is not valid!!!!!!!!!!!")
            form = forms.CustomUserRegisterForm()
            return render(request, 'usersapp/signup.html', context={"form": form})
    print("Method GET !!!!!!!!")
    form = forms.CustomUserRegisterForm()
    return render(request, 'usersapp/signup.html', context={"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
        print("Run Activate ............")
        print(user.pk)

    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        print("User Not NONE !!!!!!!!!")
        user.is_active = True
        user.save()
        return redirect('usersapp:login_user')

    else:
        print("User is NONE !!!!!!!!!!!!!!")
        return redirect('usersapp:create_user_profile')


def login_user(request):
    if request.user.is_authenticated:
        return redirect(to='usersapp:main')

    if request.method == 'POST':
        print('I\'m in POST')
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        print(user)
        if user is None:
            print('I\'m in POST but user is NONE ')
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='usersapp:login_user')

        login(request, user)
        print("You was Logged IN !!!!!!!!!!!!!!!")
        return redirect(to='usersapp:main')

    form = forms.LoginForm()
    return render(request, 'usersapp/login.html', context={"form": form})


@login_required
def logout_user(request):
    logout(request)
    return redirect(to='usersapp:login_user')


@login_required
def success(request):
    return render(request, 'usersapp/success.html')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'usersapp/password_reset.html'
    email_template_name = 'usersapp/password_reset_email.html'
    html_email_template_name = 'usersapp/password_reset_email.html'
    success_url = reverse_lazy('usersapp:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'usersapp/password_reset_subject.txt'
