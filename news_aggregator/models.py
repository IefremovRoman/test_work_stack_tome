from django.db import models


class News(models.Model):
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    published = models.CharField(max_length=32)
    trend = models.CharField(max_length=24)
