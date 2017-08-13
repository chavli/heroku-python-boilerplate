"""
    simple classes that define standardized JSON structures for responses
"""
import simplejson as json


class ResponseJson():
    __data = {}
    __code = 0

    def __init__(self, data: dict, code: int=200):
        """ define a custom JSON response and return code """

        # this code looks weird but its to properly handle data types that can't be handled
        # by the standard flask jsonify method (e.g. Decimals). so we use simplejson to dump the
        # raw json to a string (simplejson converts decimals to strings) and then load it
        # back to json for flask to take care of later
        self.data = json.loads(json.dumps(data))
        self.return_code = code

    def __str__(self):
        return json.dumps(self.__data)

    @property
    def return_code(self):
        return self.__code

    @return_code.setter
    def return_code(self, code: int):
        self.__code = code

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    def make_response(self):
        return self.__data, self.__code


class DeprecatedResponseJson(ResponseJson):
    """ return an error message telling the client they called a deprecated API """

    def __init__(self):
        super().__init__({"error": "deprecated"}, 400)


class UnimplementedResponseJson(ResponseJson):
    """ return an error message indicating endpoint is not implemented """

    def __init__(self):
        super().__init__({"exception": "unimplemented"}, 501)


class ExceptionResponseJson(ResponseJson):
    """ json structure for returning server-side errors/exceptions info to clients """

    def __init__(self, message: str, exc: Exception = None):
        super().__init__({"exception": message}, 500)


class ErrorResponseJson(ResponseJson):
    """ json structure for returning client-caused error info to clients """

    def __init__(self, message: str, err_code: int = 0):
        data = {"error": message, "error_code": err_code}
        super().__init__(data, 400)


class UnauthorizedResponseJson(ResponseJson):
    """ json structure notifying the client they're not authorized to access our stuff """

    def __init__(self):
        data = {"error": "invalid credentials"}
        super().__init__(data, 401)

    def make_response(self):
        """ override parent impl to include some special header info """
        return self.data, self.return_code, {'WWW-Authenticate': 'Basic realm="Login Required"'}


class UnauthorizedGuestResponseJson(ResponseJson):
    """ json structure notifying the client """

    def __init__(self):
        data = {"error": "guest session expired"}
        super().__init__(data, 406)

    def make_response(self):
        return self.data, self.return_code, {'WWW-Authenticate': 'Basic realm="Login Required"'}


class MessageResponseJson(ResponseJson):
    """ json structure for returning a success, an 'everything is ok', etc type of
    of message to clients. data is an optional dict that can be included in the response
    """

    def __init__(self, message: str, data: dict = None):
        payload = {"message": message}
        if data is not None:
            payload["data"] = data
        super().__init__(payload, 200)


class EmptySuccessResponseJson(ResponseJson):
    """ an empty response, containing http 204 """
    def __init__(self):
        super().__init__(None, 204)
