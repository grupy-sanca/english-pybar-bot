FROM python:3.8

RUN pip install python-telegram-bot

RUN mkdir /app
ADD . /app
WORKDIR /app

CMD python /app/bot.py
