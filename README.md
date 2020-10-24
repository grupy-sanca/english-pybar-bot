# English PyBar Bot
[![Build Status](https://travis-ci.org/grupy-sanca/english-pybar-bot.png?branch=master)](https://travis-ci.org/grupy-sanca/english-pybar-bot)

## What is English PyBar Bot?
The English PyBar Bot is a Telegram bot created to generate conversation topics for our English-hosted PyBares.

It has a list of questions that can be drawn randomly, and each participant of the session can check which question is being currently discussed or draw the next one.

## About grupy-sanca
grupy-sanca is a Python User Group from São Carlos, Brazil.

We host meetups in English at the bar to help our members improve their English conversation
skills aided by beer and good company.

## How to use
To test the bot, you'll need a token for a Telegram bot.

You can create a bot via @BotFather and it'll send you the token.

Then you'll be able to run the code in this repository in your own bot.

### Instructions

* Clone the repository and enter the folder english-pybar-bot
* Create a copy of the file `local.env` and rename it to `.env`
```
$ cp local.env .env
```
* Edit `.env` to insert your Telegram bot token
```
TOKEN=insert_your_token_here
MOD=dev
```

* Create a virtualenv to install the dependencies (we recommend `pipenv`) and activate it
```
$ pipenv install -d
$ pipenv shell
```

* Install `pre-commit` to ensure that every commit is tested against the current code conventions.
```
(venv) $ pre-commit install
```

* Run `bot.py` to start the bot
```
(venv) $ python bot.py
```

### Testing
To run the tests, use:
```
$ (venv) pytest
```

## Contribute
Feel free to contribute!

Be sure to write tests for new features (we also need help to improve our testing coverage).

**You can get in touch with us at https://t.me/grupysanca**
