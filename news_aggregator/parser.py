# -*- coding: utf-8 -*-
"""GoogleTrends_get_corresponding_news.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xnHTfUOCsHoYbER9LNiVLJ3Z8TrxNPx0

"""

# Parsing google trends

from datetime import datetime, timedelta
import json
import string

import requests
from bs4 import BeautifulSoup
import feedparser

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = stopwords.words('russian')
import pymorphy2
from nltk.tokenize import word_tokenize

nltk.download('punkt')
morph = pymorphy2.MorphAnalyzer()


def news_aggregator():
    # Forming a week date by date for trend parser link
    today = datetime.today()

    days = []
    for i in range(8):
        d = today - timedelta(days=i)
        days.append(d.strftime("%Y%m%d"))

    # Parsing trends from Google trends
    trend_list = []

    for day in days:
        link = f'https://trends.google.com/trends/api/dailytrends?hl=ru&tz=-180&ed={day}&geo=UA&ns=15'
        response = requests.get(link)

        soup = BeautifulSoup(response.content, 'html.parser')
        text = '{' + soup.text[7:]
        site_json = json.loads(text)
        trend_raw_dict = site_json['default']['trendingSearchesDays'][0]['trendingSearches']

        for trend in trend_raw_dict:
            trend_list.append(trend['title']['query'])

    # Rss news paper parser
    link = 'https://112ua.tv/rss/index.rss'

    feed = feedparser.parse(link)

    news_list = list()
    for n in feed.entries:
        news_list.append({
            'title': n.title,
            'link': n.link,
            'published': n.published
        })

    news_titles = list()
    for entry in feed.entries:
        news_titles.append(entry.title)

    # Text clean
    def clean_string(text_string):
        digits = [str(i) for i in range(10)]
        text_string = ''.join([word for word in text_string if (word not in digits)])
        text_string = text_string.lower()
        text_string = ''.join([word for word in text_string if word not in string.punctuation + '–'])
        text_string = ' '.join([word for word in text_string.split() if (word not in stop_words)])

        return text_string

    cleaned_trends = list(map(clean_string, trend_list))
    cleaned_news = list(map(clean_string, news_titles))

    # Tokenize and stemming our news dataset
    def preprocess(tokens):
        return [morph.normal_forms(word)[0] for word in tokens]

    prepared_trends = cleaned_trends.copy()

    prepared_news = list(
        map(
            preprocess,
            [word_tokenize(word, language='russian') for word in cleaned_news]
        )
    )
    prepared_news = [' '.join(sentence) for sentence in prepared_news]
    corpus = prepared_trends + prepared_news

    # Vectorizer modelling
    vectorizer_of_corpus = CountVectorizer().fit_transform(corpus)
    vectors_of_corpus = vectorizer_of_corpus.toarray()

    # Dividing trends and news separetly
    vectors_of_trends = vectors_of_corpus[:len(prepared_trends) + 1]
    vectors_of_news = vectors_of_corpus[len(prepared_trends):]

    # Finding cosine similarity and reshaping function:
    def cosine_sim_vectors(vec_a, vec_b):
        vec_a = vec_a.reshape(1, -1)
        vec_b = vec_b.reshape(1, -1)
        return cosine_similarity(vec_a, vec_b)[0][0]

    # Treating our dataset
    treshold = 0.26
    correspondings = {}
    list_correspondings = []

    for trend_v, trend in zip(vectors_of_trends, trend_list):
        for news_v, news in zip(vectors_of_news, news_list):
            cos_sim = cosine_sim_vectors(trend_v, news_v)
            if cos_sim > treshold:
                correspondings[trend] = news['title']
                list_correspondings.append({
                    'title': news['title'],
                    'link': news['link'],
                    'published': news['published'],
                    'trend': trend
                })

    return list_correspondings, trend_list