"""
    log of all endpoint hits and their return errors
"""
import datetime
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql as pgsql
from sqlalchemy.schema import Sequence
from . import Base

class EndpointLog(Base):
    """ a table that keeps track of endpoint hits """
    __tablename__ = "endpoint_log"
    __table_args__ = ()

    id = Column(pgsql.INTEGER, Sequence("endpoint_log_id_seq"), primary_key=True)
    start_epoch_utc = Column(pgsql.NUMERIC(14, 3), nullable=False)
    duration_ms = Column(pgsql.INTEGER, nullable=False)
    endpoint = Column(pgsql.TEXT)
    username = Column(pgsql.TEXT)
    method = Column(pgsql.TEXT)
    http_code = Column(pgsql.TEXT)
    error_message = Column(pgsql.TEXT)

    def __init__(self, start_epoch_utc: float, duration_ms: int, endpoint: str,
                 username: str, method: str, http_code: int, error_message: str=None):
        self.start_epoch_utc = start_epoch_utc
        self.duration_ms = duration_ms
        self.endpoint = endpoint
        self.username = username
        self.method = method
        self.http_code = http_code
        self.error_message = error_message

    def __str__(self):
        return "[{start_utc}]{username}: {method} {endpoint} HTTP: {http_code}".format(**{
            "start_utc": datetime.datetime.utcfromtimestamp(self.start_epoch_utc),
            "username": self.username,
            "method": self.method,
            "endpoint": self.endpoint,
            "http_code": self.http_code,
            })
