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

from .scrap_news import *


@login_required
def choice_topic(request, q):
    list_res = []
    match q:
        case 'war_in_ukraine':
            list_res = news_war()
        case 'business':
            list_res = news_business()
        case 'since':
            list_res = news_since()

    return render(request, 'newsapp/read_news.html', {"text": list_res})


@login_required
def paragraph(request, q):
    title, text, picture = parse_page(q)
    context = {
        'title': title,
        'content': text,
        'picture': picture,
    }
    return render(request, 'newsapp/detail_paragraph.html', context)
