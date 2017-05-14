from sqlalchemy import Column
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import postgresql as pgsql
from . import Base

class SessionToken(Base):
    __tablename__ = "session_token"

    id = Column(pgsql.INTEGER, primary_key=True)
    user_id = Column(pgsql.TEXT)
    token = Column(pgsql.TEXT)
    created_utc = Column(pgsql.TIMESTAMP, server_default=func.now())

    def __init__(self, user_id: str, token: str):
        self.user_id = user_id
        self.token = token
