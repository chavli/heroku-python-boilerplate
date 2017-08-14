"""
    custom function decorators
"""
import traceback
import imghdr
from werkzeug.exceptions import BadRequest
from functools import wraps
from flask import request, Response
from .requestparser import RequestParser
from ..core.utils.responsejson import *
from ..managers.sessionmanager import SessionManager
from ..managers.accountmanager import AccountManager


def validate_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            request.json
            if request.json is None:
                return ErrorResponseJson("Content-Type=application/json required").make_response()
        except BadRequest as e:
            return ErrorResponseJson("payload must be a valid json").make_response()
        return func(*args, **kwargs)
    return wrapper


def validate_jpeg_binary(func):
    """ checks the mimetype and the binary data to ensure it's a JPEG """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.content_type != "image/jpeg":
            return ErrorResponseJson("invalid content type: {}".format(request.content_type)).make_response()
        if imghdr.test_jpeg(request.data, None) != "jpeg":
            return ErrorResponseJson("invalid jpeg data").make_response()
        return func(*args, **kwargs)
    return wrapper


def require_auth_header(func):
    """ no auth check is performed but the auth headers are still required. auth check
    is performed by a service other than ourselves """
    @wraps(func)
    def decorator(*args, **kwargs):
        if not request.authorization:
            return ErrorResponseJson("auth header required").make_response()
        return func(*args, **kwargs)
    return decorator


def no_authorization(func):
    """ no auth check. used to indicate endpoints that have no authentication such as
    account creation """
    @wraps(func)
    def decorator(*args, **kwargs):
        return func(*args, **kwargs)
    return decorator


def require_token(func):
    """ verifies the uuid/token combo of the given account. account type can be:
        customer, fox, merchant """
    @wraps(func)
    def decorator(*args, **kwargs):
        if request.authorization:
            uuid = request.authorization.username
            token = request.authorization.password
            try:
                manager = SessionManager()
                valid = manager.verify(uuid, token)
                if not valid:
                    return UnauthorizedResponseJson().make_response()
            except Exception as e:
                traceback.print_exc()
                return ExceptionResponseJson("unable to validate credentials", e).make_response()
        else:
            return UnauthorizedResponseJson().make_response()
        return func(*args, **kwargs)
    return decorator


def require_password(func):
    """ verifies the given username/password combo """
    @wraps(func)
    def decorator(*args, **kwargs):
        if request.authorization:
            username = request.authorization.username
            password = request.authorization.password
            try:
                manager = AccountManager()
                valid = manager.verify_account(username, password)
                if not valid:
                    return UnauthorizedResponseJson().make_response()
            except Exception as e:
                traceback.print_exc()
                return ExceptionResponseJson("unable to validate credentials", e).make_response()
        else:
            return UnauthorizedResponseJson().make_response()
        return func(*args, **kwargs)
    return decorator
