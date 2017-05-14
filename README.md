# Introduction
You scream, I scream, we all scream for REST API's! Whether for fun or for work a REST API exposes
backend resources to frontend clients.

I've always wanted to open up the framework I use to create APIs for two reasons: first, it's a pain to have
to write basic functionality over and over when creating multiple APIs, and secondly to serve as a
learning resouce for others. Therefore, what I have here is as much for me as it is for all of you:
a quick way to get your API up and running so you can build your app and not worry about the overhead of setting
up really basic code components.

The code here is the result of my experience working on REST API's over several years both professionally
and for fun. It's evolved over the years and I feel it's at a good place to share. I expect to it change
more in the future.

# Requirements
* Python 3.6.1+
* `virtualenv` and `pip`: managing local development environment
* [Heroku Toolbelt](https://devcenter.heroku.com/articles/heroku-cli): Heroku CLI

# Optional
- [Postman](https://www.getpostman.com/) -- Cool tool for testing REST API's

# Included Features:
The code as is comes with these features already built in:
* pre-configured to be deployed to a Heroku app with a PostgreSQL database
* pre-defined sample endpoints and account management endpoints
* application logic for handling user account creation and sessions
* predefined `SQLAlchemy` model classes for user accounts, user sessions, and logging
* function decorators for endpoint authentication and JSON validation
* JWT generation / verification
* hash generation / verification using `pbkdf2_sha256`
* `RequestParser`: a class that makes it easy to define, enforce, and parse endpoint parameters
* `ResponseJson`: a class that standardizes the JSON format of endpoint responses
* `SQLAlchemy` session management
* a light wrapper around `psycopg2` for handling custom queries and connection management
* a `Logger` class for writing application logs and endpoint hit logs to a pre-defined table
* `Alembic` pre-configured to initlaize and upgrade database schemas


# Setup Instructions

```
git clone https://github.com/chavli/heroku-python-skeleton.git .
```

## Heroku Setup
```{bash}
heroku login
heroku apps:create your_app_name
heroku config:set JWT_SECRET="secret value!" --app your_app_name
heroku config:set JWT_ISS="secret value!" --app your_app_name
git remote add heroku git@heroku.com:your_app_name.git
heroku addons:create heroku-postgresql --app your_app_name
```

## Local Environment
```{bash}
virtualenv venv -p /usr/bin/python3.6
source venv/bin/activate
pip install -r requirements.txt

heroku config --app your_app_name --shell > .env
cp .env .bash_env
```

## Initializing the Database (optional)
```
source .bash_env
alembic upgrade head
```

## Testing Locally
```
heroku local web
python rundebug.py
```

# Core Libraries
* [Flask](http://flask.pocoo.org/)
* [Flask-Restful](https://flask-restful.readthedocs.io/en/0.3.5/)
* [Waitress](http://docs.pylonsproject.org/projects/waitress/en/latest/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Alembic](http://alembic.zzzcomputing.com/en/latest/)
* [psycopg2](http://initd.org/psycopg/)

# Out-of-the-box Endpoints

- `GET /api/hello`
- `GET /api/echo`
- `GET /api/protectedhello`
- `POST /api/account`
- `GET /api/session`
- `DELETE /api/session`


# Advanced

## Updating the Schema
```
alembic revision --autogenerate -m "update details"
alembic upgrade head
```
