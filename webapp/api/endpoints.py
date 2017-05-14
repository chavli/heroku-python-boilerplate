"""
    define the api routes for your classes
"""

from flask import Blueprint
from flask_restful import Api

from .account import Account
from .session import Session
from .hello import HelloWorld, EchoWorld, ProtectedWorld

# endpoint routing errors, not the same as application level errors handled by the ResponseJson class
errors = {
    "Unauthorized": {
        "error": "Unauthorized Access",
        "status": 401
        },
    "NotFound": {
        "error": "Endpoint Not Found",
        "status": 404
        },
    "MethodNotAllowed": {
        "error": "Method Not Allowed",
        "status": 405
        }
}

demo_blueprint = Blueprint("demo_api", __name__)
demo_api = Api(demo_blueprint, errors=errors)

demo_api.add_resource(HelloWorld,"/hello")
demo_api.add_resource(EchoWorld,"/echo")
demo_api.add_resource(ProtectedWorld,"/protectedhello")
demo_api.add_resource(Account,"/account")
demo_api.add_resource(Session,"/session")

