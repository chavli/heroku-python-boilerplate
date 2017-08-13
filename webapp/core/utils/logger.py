"""
    simple logging framework used by the fetchy backend
"""
import hashlib
import time
import traceback
import inspect
from .dbsession import dbsession
from ..models.systemlog import SystemLog, LogLevel
from ..models.endpointlog import EndpointLog


class Logger():

    @classmethod
    def __write_syslog(cls, level: LogLevel, message: str, session=None):
        frame, file_name, line_number, func_name, lines, index = inspect.stack()[2]
        source = "{filepath}:{funcname}({line_num})".format(**{
            "filepath": file_name,
            "funcname": func_name,
            "line_num": line_number,
            })

        syslog = SystemLog(level, source, message)
        print(syslog)
        if session:
            session.add(syslog)
            session.commit()
            sid = syslog.id
        else:
            with dbsession() as session:
                session.add(syslog)
                session.commit()
                sid = syslog.id

        return sid

    @classmethod
    def __write_eplog(cls, eplog: EndpointLog, session=None):
        if session:
            session.add(eplog)
        else:
            with dbsession() as session:
                session.add(eplog)

    @classmethod
    def start(cls, existing_session=None):
        """ mark the start of some event. returns a unique id """
        eid = hashlib.md5(str(time.time()).encode()).hexdigest()
        frame, file_name, line_number, func_name, lines, index = inspect.stack()[1]
        cls.__write_syslog(LogLevel.START_EVENT, "[{eid}] starting".format(**{
            "eid": eid,
            }), existing_session)
        return eid

    @classmethod
    def end(cls, event_id: str, existing_session=None):
        """ mark the end of some event. requires the events id """
        frame, file_name, line_number, func_name, lines, index = inspect.stack()[1]
        cls.__write_syslog(LogLevel.END_EVENT, "[{eid}] ending".format(**{
            "eid": event_id,
            }), existing_session)

    @classmethod
    def debug(cls, message: str, existing_session=None):
        """ messages used during dev/debug """
        cls.__write_syslog(LogLevel.DEBUG, message, existing_session)

    @classmethod
    def info(cls, message: str, existing_session=None):
        """ important events / info. errors caused by clients. lifecycle events. etc """
        cls.__write_syslog(LogLevel.INFO, message, existing_session)

    @classmethod
    def warn(cls, message: str, exc: Exception=None, existing_session=None) -> int:
        """ server-side non-critical/unexpected/business-logic errors.
        system continues working, however. """
        if exc:
            traceback.print_exception(type(exc), exc, None)
        return cls.__write_syslog(LogLevel.WARN, message, existing_session)

    @classmethod
    def error(cls, message: str, exc: Exception, existing_session=None) -> int:
        """ something that if you saw at 4AM you would wake up immediately to fix """
        traceback.print_exception(type(exc), exc, None)
        return cls.__write_syslog(LogLevel.ERROR, message, existing_session)

    @classmethod
    def critical(cls, message: str, exc: Exception, existing_session=None) -> int:
        """ an unexpected mission-critical error caused by something outside our control. get into
        contact immediately. triage issue right away. """
        traceback.print_exception(type(exc), exc, None)
        return cls.__write_syslog(LogLevel.CRITICAL, message, existing_session)

    @classmethod
    def endpoint_hit(cls, start_epoch_utc: float, duration_ms: int, endpoint: str,
                     auth_username: str, method: str, http_code: int, error_message: str=None,
                     existing_session=None):
        log = EndpointLog(start_epoch_utc, duration_ms, endpoint, auth_username, method, http_code,
                          error_message)
        cls.__write_eplog(log, existing_session)
