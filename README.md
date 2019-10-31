# English PyBar Bot

[![Build Status](https://travis-ci.org/grupy-sanca/english-pybar-bot.png?branch=master)](https://travis-ci.org/grupy-sanca/english-pybar-bot)

## What

Bot created to generate conversation topics for our English-hosted PyBares.

## Why

grupy-sanca is a Python User Group from São Carlos, Brazil, and we host meetups
in English at the bar to help our members improve their English conversation
skills, aided by beer and good company.

## How to use

First clone the repository then `cd` inside.
Then install dependencies, enter virtualenv and install pre-commit

```
pipenv install -d
pipenv shell
(venv) $ pre-commit install
```

pre-commit is used to ensure every commit is tested against the current
code conventions.

The local.env has the basic ENV list for the bot to work
```
cp local.env .env
```

then edit .env with the correct values.

### To run the tests, run

```
(venv) $ pytest
```

After each new feature make sure to write tests for that feature.

## Contribute

Feel free to contribute!
