"""
    log dump for our backend code
"""
import datetime
from enum import unique, auto
from sqlalchemy import Column
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql as pgsql
from sqlalchemy.schema import Sequence
from ..utils.autonamedenum import AutoNamedEnum
from . import Base


@unique
class LogLevel(AutoNamedEnum):

    # messages used during dev/debug
    # NOTE: printing state of code
    DEBUG = auto()

    # important events / info. errors caused by clients. lifecycle events. etc
    # NOTE: bad user credentials. scheduled script starts running.
    INFO = auto()

    # server-side non-critical/unexpected/business-logic errors. system continues working, however.
    # NOTE: nightly job fails to complete. emails fail to go out
    WARN = auto()

    # something that if you saw at 4AM you would wake up immediately to fix
    # NOTE: an exception occurs that keeps the system from operating
    ERROR = auto()

    # a critical error caused by something outside our control. get into contact immediately
    # NOTE: AWS goes down
    CRITICAL = auto()


class SystemLog(Base):
    """ a single log """
    __tablename__ = "system_log"
    __table_args__ = ()

    _ID_SEQ = Sequence("system_log_id_seq")
    id = Column(pgsql.INTEGER, _ID_SEQ, server_default=_ID_SEQ.next_value(), primary_key=True,
                nullable=False)
    event_utc = Column(pgsql.TIMESTAMP(timezone=False), server_default=func.now(), nullable=False)
    level = Column(pgsql.TEXT)
    message = Column(pgsql.TEXT)
    source = Column(pgsql.TEXT)

    def __init__(self, level: LogLevel, source: str, message: str):
        self.source = source
        self.message = message
        self.level = repr(level)
        self.event_utc = datetime.datetime.utcnow()

    def __str__(self):
        return "[{event_utc} {level}] {source}: {message}".format(**{
            "event_utc": self.event_utc,
            "level": self.level,
            "source": self.source,
            "message": self.message,
            })
