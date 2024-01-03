from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views

app_name = 'newsapp'

urlpatterns = [
    path('read_news/<str:q>/', views.choice_topic, name="read_news"),
    path('detail_paragraph/<str:q>/', views.paragraph, name="detail_paragraph"),
    ]
