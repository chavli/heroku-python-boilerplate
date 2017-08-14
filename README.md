(Draft) The instructions work they just need to be polished.

# Introduction
You scream, I scream, we all scream for REST API's! Whether for fun or for work a REST API exposes
backend resources to frontend clients. If you have even a little development experience then you can
have a working API **deployed in minutes!**

You can even expand this example into production ready code!

## Motivation and Purpose
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


## Requirements
* Python 3.6.1+
* `virtualenv` and `pip`
* A free Heroku account
* [Heroku Toolbelt](https://devcenter.heroku.com/articles/heroku-cli)

## Optional
- [Postman](https://www.getpostman.com/) -- Cool tool for testing REST API's
- [DBeaver](http://dbeaver.jkiss.org/) -- a cross-platform database client that works with practically every database

## Included Features:
The code as-is comes with these features already built in:
- General
    * pre-configured to be deployed to a Heroku app with a PostgreSQL database
    * pre-defined sample endpoints and account management endpoints
    * application logic for handling user account creation and sessions
- Utilities
    * `RequestParser`: a class that makes it easy to define, enforce, and parse endpoint parameters
    * `ResponseJson`: a class that standardizes the JSON format of endpoint responses
    * a `Logger` class for writing application logs and endpoint hit logs to a pre-defined table
- Database
    * `Alembic` pre-configured to initialize and upgrade database schemas
    * pre-defined `SQLAlchemy` model classes for user accounts, user sessions, and logging
    * `SQLAlchemy` database session management
    * a light wrapper around `psycopg2` for handling custom queries and connection management
- Authentication and Security
    * function decorators for endpoint authentication and JSON validation
    * AES encrypt / decrypt
    * hash generation / verification using `pbkdf2_sha256` (storing password)
    * JWT generation / verification

## Setup Instructions

### Heroku Setup
You can do all this through the Heroku dashboard but it's quicker to do it all through
your terminal. The following commands create your Heroku app, configure a few variables,
and attach a PostgreSQL database. Replace `your_app_name` with anything you want.
`JWT_SECRET` can be set to any value, this is used to create web tokens. `JWT_ISS`
can also be set to any value and represents who is _issuing_ the token.

```{bash}
heroku login
heroku apps:create your_app_name
heroku config:set JWT_SECRET="shh secret value!" --app your_app_name
heroku config:set JWT_ISS="project/team name" --app your_app_name
heroku addons:create heroku-postgresql --app your_app_name
```

### Local Environment
Great, now lets setup your local environment for development!

Create a folder (the root folder of your project), and go into it:
```
git clone https://github.com/chavli/heroku-python-boilerplate.git .
git remote add heroku git@heroku.com:your_app_name.git
```

Once you have the code, you have to create a virtual environment and install dependencies:
```{bash}
virtualenv venv -p /usr/bin/python3.6
source venv/bin/activate
pip install -r requirements.txt
```
In the future, before working on your local copy of the code, make sure you're in the virtual environment by executing `source venv/bin/activate` from the root folder.

Now you need a local copy of all the environment variables your Heroku app has:
```
heroku config --app your_app_name --shell > .env
cp .env .bash_env
```
You'll have to manually prepend `export ` to each line in `.bash_env`.


### Initializing the Database
The last step! These commands will create 4 tables in the PostgreSQL database for tracking accounts,
sessions, and various logs:
```
source .bash_env
alembic upgrade head
```

### Testing Locally
Running either of these commands will start a local server on `localhost:5000`. If everything works then going to
`localhost:5000/api/hello` will return `{"hello": "world"}`
```
heroku local web
- OR -
python rundebug.py
```

### Deploying your Code
Now it's time for the main attraction! Pushing your code to Heroku and making it live!
Commit any changes you made, if any, and push it directly to Heroku:
```
git push heroku master
```

In minutes your endpoints will be live on: `https://your_app_name.herokuapp.com`


## Out-of-the-box Endpoints

- `GET /api/hello`: a simple "hello world" endpoint
- `GET /api/echo`: illustrates how to parse URL parameters
- `GET /api/protectedhello`: illustrates how to protect endpoints with user accounts
- `POST /api/account`: create a new user account
- `GET /api/session`: alogin with an existing account
- `DELETE /api/session`: logout

Postman is the easiest way to test these endpoints.

## Core Libraries
* [Flask](http://flask.pocoo.org/)
* [Flask-Restful](https://flask-restful.readthedocs.io/en/0.3.5/)
* [Waitress](http://docs.pylonsproject.org/projects/waitress/en/latest/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Alembic](http://alembic.zzzcomputing.com/en/latest/)
* [psycopg2](http://initd.org/psycopg/)




## Advanced

### Updating the Schema
```
alembic revision --autogenerate -m "update details"
alembic upgrade head
```
