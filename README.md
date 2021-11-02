# News aggregator

## Task

1. Imagine that we want to make a news aggregator that will take news from a large site (for example, 112.ua) but only show news matches who are currently in trend. To do this, you are invited to build a prototype system that will regularly update the stream from 112's RSS feeds (https://112.ua/rsslist - if you have other preferences in the news world - you can choose another source of the same size) and highlight the news that is currently in the trend for the last 7 days according to Google (pull last 7 days data from using api or rss, https://trends.google.com/trends/trendingsearches/daily?geo=UA). The system should thus maintain an up-to-date data mart, from which you can take news for display to the user at any time, data should be refetched every 1 min.

2. The prototype must be provided in the form of source codes and launch instructions. Ideally, the system will run in the format of docker-containers.

3. You do not need to do a complex text analysis when searching for matches of the text of news and trends - it will be enough to clear the text from special characters and bring it to lower case.

4. You do not need to make a UI to view the news / system management - a brief description of how to see the showcase of relevant ("in trend") news will suffice. For each news there will be enough a headline, links to the source, dates of publication of the news and the names of the trend.

5. It is allowed to use any Python-related technological stack - Python, Django, Celery, you can also use any client libraries that can help you to parse/get data from given sources

6. Code should be put on github repo.

## Usage:

- Just type `docker-compose up`

- Go to localhost:8000
