from django.core.mail import EmailMessage

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site

# from ..tokens import account_activation_token
from .scrap_news import *




@login_required
def choice_topic(request, q):
    print(q)
    list1 = []

    if q == 'war_in_ukraine':
        list1 = news_war()
        
    elif q == 'business':
         list1 = news_business()

    elif q == 'since':
         list1 = news_since()

    elif q == '':
         list1 = news_business()

    return render(request, 'newsapp/read_news.html', {"text": list1})


@login_required
def paragraph(request, q):
 
    title, text, picture = parse_page(q)
    print(f'Text: : : :  {text}')
    context = {
        'title': title,
        'content': text,
        'picture': picture,
    }
    print(f"CONTENT   ::::   {context}")
    return render(request, 'newsapp/detail_paragraph.html', context)

   