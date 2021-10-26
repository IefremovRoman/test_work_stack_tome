from django.shortcuts import render
from django.views.generic import ListView

from .models import News


class NewsListView(ListView):
    model = News
    template_name = 'news_list.html'
