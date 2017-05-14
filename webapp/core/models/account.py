"""
    object model rep of an user account
"""
from sqlalchemy import Column
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql as pgsql
from sqlalchemy.schema import Sequence
from sqlalchemy.ext.declarative import declarative_base
from ..utils.basics import prefixed_uuid4
from ..models import Base

class Account(Base):
    __tablename__ = "user_account"

    id = Column(pgsql.INTEGER, Sequence("user_account_id_seq"), primary_key=True, nullable=False)
    user_id = Column(pgsql.TEXT)
    email = Column(pgsql.TEXT)
    secret = Column(pgsql.TEXT)
    creation_utc = Column(pgsql.TIMESTAMP, server_default=func.now())
    last_updated_utc = Column(pgsql.TIMESTAMP, server_default=func.now())


    def __init__(self, email: str, secret: str):
        self.user_id = prefixed_uuid4("usr")
        self.email = email
        self.secret = secret
