"""
    simple logging framework used by the fetchy backend
"""
import traceback
import inspect
import datetime as dt
from .dbsession import dbsession
from ..models.systemlog import SystemLog, LogLevel
from ..models.endpointlog import EndpointLog


class Logger():

    @classmethod
    def __write_syslog(cls, level: LogLevel, message: str):
        frame, file_name, line_number, func_name, lines, index = inspect.stack()[2]
        source = "{filepath}:{funcname}({line_num})".format(**{
            "filepath": file_name,
            "funcname": func_name,
            "line_num": line_number,
            })

        syslog = SystemLog(level, source, message)
        print(syslog)
        with dbsession() as session:
            session.add(syslog)

    @classmethod
    def __write_eplog(cls, eplog: EndpointLog):
        with dbsession() as session:
            session.add(eplog)

    @classmethod
    def debug(cls, message: str):
        cls.__write_syslog(LogLevel.DEBUG, message)

    @classmethod
    def info(cls, message: str):
        cls.__write_syslog(LogLevel.INFO, message)

    @classmethod
    def warn(cls, message: str):
        cls.__write_syslog(LogLevel.WARN, message)

    @classmethod
    def error(cls, message: str, exc: Exception):
        traceback.print_exception(type(exc), exc, None)
        cls.__write_syslog(LogLevel.ERROR, message)

    @classmethod
    def critical(cls, message: str, exc: Exception):
        traceback.print_exception(type(exc), exc, None)
        cls.__write_syslog(LogLevel.CRITICAL, message)

    @classmethod
    def endpoint_hit(cls, start_epoch_utc: float, duration_ms: int, endpoint: str,
            auth_username: str, method: str, http_code: int, error_message: str=None):
        log = EndpointLog(start_epoch_utc, duration_ms, endpoint, auth_username, method, http_code,
                error_message)
        cls.__write_eplog(log)
