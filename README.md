# Introduction
You scream, I scream, we all scream for REST API's! Whether for fun or for work a REST API exposes
backend resources to frontend clients. If you have even a little development experience then you can
have a working API **deployed in minutes!**

# Motivation and Purpose
I've noticed over the years of working on backend code that there aren't many meaningful examples
of backend code that illustrates how everything works together.Of course, there are countless code pieces
 showing discrete parts of a functional backend and even small examples of a working
 "hello world" endpoint but it's still up to the developer to tie these pieces together, and
 configure, anything meaningful. Not everything is hopeless, however. Companies are making it easier to setup your own server [references needed] and creating the tools
 to easily deploy live code but the question still remains _what code do you deploy?_

This is the question I want to try to answer. I think this disconnect contributes to an environment
that makes it hard to learn backend development and encourages a misconception that backend code is
"hard" or "confusing".

I want to achieve a few things by sharing this code:
1. create a non-trivial, but still minimal, codebase illustrating some core concepts of REST API development and tieing them together
2. demonstrate the process of deploying code to a live environment, in this case to Heroku.
3. save myself, and others, time when it comes to setting up a backend for hackathons and small projects.


# Requirements
* Python 3.6.1+
* `virtualenv` and `pip`
* [Heroku Toolbelt](https://devcenter.heroku.com/articles/heroku-cli)

# Optional
- [Postman](https://www.getpostman.com/) -- Cool tool for testing REST API's

# Included Features:
The code as-is comes with these features already built in:
* pre-configured to be deployed to a Heroku app with a PostgreSQL database
* pre-defined sample endpoints and account management endpoints
* application logic for handling user account creation and sessions
* pre-defined `SQLAlchemy` model classes for user accounts, user sessions, and logging
* function decorators for endpoint authentication and JSON validation
* `RequestParser`: a class that makes it easy to define, enforce, and parse endpoint parameters
* `ResponseJson`: a class that standardizes the JSON format of endpoint responses
* a `Logger` class for writing application logs and endpoint hit logs to a pre-defined table
* `SQLAlchemy` database session management
* a light wrapper around `psycopg2` for handling custom queries and connection management
* `Alembic` pre-configured to initialize and upgrade database schemas
* JWT generation / verification
* hash generation / verification using `pbkdf2_sha256`


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
