from flask import request
from flask_restful import Resource
from ..core.utils.responsejson import ResponseJson, MessageResponseJson
from ..extensions.decorators import require_password
from ..extensions.requestparser import RequestParser 


class HelloWorld(Resource):
    """ hello, world! if this endpoint works then yaaay your code deploys correctly """

    def get(self):
        r = ResponseJson({"message": "hello, world"})
        return r.make_response()


class EchoWorld(Resource):
    """ this is an example of how to parse URL parameters """

    def get(self):
        parser = RequestParser()
        parser.add_argument("message", type=str, required=True, location="args")
        parser.add_argument("number", type=int, required=False, location="args")
        parser.add_argument("vote", type=str, required=False, choices=("red", "blue", "green"),
                location="args")
        args = parser.parse_args()

        data = {
            "number": args.number if args.number else None,
            "vote": args.vote if args.vote else None,
            }
        
        r = MessageResponseJson(args.message, data)
        return r.make_response()


class ProtectedWorld(Resource):
    """ this is an example of an endpoint that requires credentials """

    @require_password 
    def get(self):
        r = ResponseJson({"message": "hello, world"})
        return r.make_response()

