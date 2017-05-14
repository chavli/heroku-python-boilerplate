"""
    object model rep of an user account
"""
import datetime
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql as pgsql
from sqlalchemy.schema import Sequence
from sqlalchemy.ext.declarative import declarative_base
from ..utils.basics import prefixed_uuid4
from ..models import Base

class Account(Base):
    __tablename__ = "user_account"

    id = Column(pgsql.INTEGER, Sequence("user_account_id_seq"))
    user_id = Column(pgsql.TEXT, primary_key=True, default=prefixed_uuid4("usr"))
    email = Column(pgsql.TEXT)
    secret = Column(pgsql.TEXT)
    creation_utc = Column(pgsql.TIMESTAMP, default=datetime.datetime.utcnow)
    last_updated_utc = Column(pgsql.TIMESTAMP, default=datetime.datetime.utcnow)


    def __init__(self, email: str, secret: str):
        self.user_id = prefixed_uuid4("usr")
        self.email = email
        self.secret = secret
