from flask import request
from flask_restful import Resource
from ..core.utils.responsejson import ErrorResponseJson, ExceptionResponseJson
from ..extensions.requestparser import RequestParser
from ..extensions.decorators import require_auth_header, validate_json
from ..managers.accountmanager import AccountManager


class Account(Resource):

    @require_auth_header
    def post(self):
        """ create a new user account """
        try:
            email = request.authorization.username
            password = request.authorization.password

            acct_manager = AccountManager()
            result = acct_manager.create(email, password)
            return result.make_response()

        except KeyError as e:
            return ErrorResponseJson("missing required key: {}".format(str(e))).make_response()
        except Exception as e:
            return ExceptionResponseJson(str(e), e).make_response()

