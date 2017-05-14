import os
import time
import datetime
from flask import Flask, request, jsonify, g
from flask_restful import Resource, Api
from .api.endpoints import demo_blueprint
from .core.utils.responsejson import ErrorResponseJson
from .core.utils.logger import Logger

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

    # log the endpoint hit and any errors
    delta = int((time.time() - g.start_time) * 1000)
    start_utc = datetime.datetime.utcfromtimestamp(g.start_time)
    username = request.authorization.username if request.authorization else None
    err_msg = response.get_data(as_text=True) if response.status_code // 100 >= 4 else None
    Logger.endpoint_hit(start_utc, delta, request.base_url, username, request.method,
                        response.status_code, err_msg)
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

