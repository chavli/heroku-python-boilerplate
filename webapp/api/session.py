"""
    sessions formally define "logging in" and "logging out"
"""
from flask import request
from flask_restful import Resource
from ..core.utils.responsejson import ExceptionResponseJson
from ..extensions.requestparser import RequestParser
from ..extensions.decorators import require_token, require_auth_header
from ..managers.accountmanager import AccountManager


class Session(Resource):

    @require_auth_header
    def get(self):
        """ create a new session for this user (login). the returned token and uuid are 
        required for future api calls """
        try:
            email = request.authorization.username
            password = request.authorization.password

            acct_manager = AccountManager()
            result = acct_manager.login(email, password)
            return result.make_response()

        except Exception as e:
            return ExceptionResponseJson(str(e), e).make_response()


    @require_token
    def delete(self):
        """ delete the given session token. (logout) """
        try:
            user_id = request.authorization.username
            token = request.authorization.password

            acct_manager = AccountManager()
            result = acct_manager.logout(user_id, token)
            return result.make_response()

        except Exception as e:
            return ExceptionResponseJson(str(e), e).make_response()

