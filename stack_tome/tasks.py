from datetime import datetime, timedelta

from celery import shared_task

from django.core.mail import send_mail

from news_aggregator.parser import news_aggregator
from news_aggregator.models import News


@shared_task
def add_news():
    news = news_aggregator()[0]
    print(f'the news!~ {len(news)}')
    print(news)
    added_news_count = 0
    for new in news:
        if not News.objects.filter(**new).exists():
            News(**new).save()
            added_news_count += 1

    return f'{added_news_count} news added'


@shared_task
def delete_news():
    trends = news_aggregator()[1]
    query = News.objects.all()
    for q in query:
        if q.trend not in trends:
            News.objects.filter(trend=q.trend).delete()

    return 'News deleted'
