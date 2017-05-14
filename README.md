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


# The Details
This is a Python backend built using Flask-Restful, Waitress, and Alembic meant to be deployed to Heroku with
a PostgreSQL database.

# Included Features:
In my experience writing API's there is always a set of core functionality that I end up re-writing or
copying from previous projects. These functions include:

1. a consistent and safe way to execute queries against a database
2. a consistent way to maintain and update your database schema
4. endpoint authentication


# heroku-python-skeleton
All the basic code to start a Python Heroku app with a PostgreSQL database.
