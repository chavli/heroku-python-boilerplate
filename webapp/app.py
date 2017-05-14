import os
import time
from flask import Flask, request, jsonify, g
from flask_restful import Resource, Api
from .api.endpoints import demo_blueprint
from .core.utils.responsejson import ErrorResponseJson

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_RECORD_QUERIES"] = True

@app.before_request
def before_request():
    """ called before every request """
    g.start_time = time.time()

@app.after_request
def after_request(response):
    """ called after every request """
    delta = time.time() - g.start_time
    print(delta)

    return response

@app.errorhandler(401)
def unauthorizedAccess(error):
    json_resp, http_code = ErrorResponseJson("Unauthorized Access").make_response()
    return jsonify(json_resp), 401


@app.errorhandler(404)
def pageNotFoundError(error):
    json_resp, http_code = ErrorResponseJson("HTTP Page Not Found").make_response()
    return jsonify(json_resp), 404


@app.errorhandler(405)
def invalidMethod(error):
    json_resp, http_code = ErrorResponseJson("HTTP Method Not Allowed").make_response()
    return jsonify(json_resp), 405


# register endpoint blueprints
app.register_blueprint(demo_blueprint, url_prefix="/api")

