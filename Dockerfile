# syntax=docker/dockerfile:1
FROM smizy/scikit-learn:latest
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apk add --update --no-cache g++ gcc libxslt-dev libxml2-dev postgresql-dev python3-dev
RUN pip install -r requirements.txt
COPY . /code/
