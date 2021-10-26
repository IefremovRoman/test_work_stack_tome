from django.contrib import admin

from news_aggregator.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ("title", "link", "published", "trend")
    list_filter = ("trend", )
    search_fields = ("trend__startswith", "title__startswith")
