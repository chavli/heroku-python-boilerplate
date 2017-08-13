import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Sessions and Connections
# https://stackoverflow.com/questions/34322471/sqlalchemy-engine-connection-and-session-difference
#
# Sessions use the Query API, an abstraction of query statements, to execute instructions:
# http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.update
#
# Connections allow you to execute statements, and raw sql, to execute instructions.
# http://docs.sqlalchemy.org/en/latest/core/expression_api.html

class MissingDatabaseException(Exception):
    def __init__(self):
        super(MissingDatabaseException, self).__init__("Database Not Initialized")


_session_factory = None
_ro_session_factory = None

if "DATABASE_URL" in os.environ:
    _engine = create_engine(os.getenv("DATABASE_URL"), convert_unicode=True)
    _session_factory = sessionmaker(bind=_engine)

if "DATABASE_RO_URL" in os.environ:
    _ro_engine = create_engine(os.getenv("DATABASE_RO_URL"), convert_unicode=True)
    _ro_session_factory = sessionmaker(bind=_ro_engine)


def _configure_session(factory, autocommit, autoflush, expire_on_commit):
    if factory:
        s = scoped_session(factory)
        s.configure(autocommit=autocommit,
                    autoflush=autoflush,
                    expire_on_commit=expire_on_commit)
        return s
    else:
        raise MissingDatabaseException()


def create_read_session(autocommit=False, autoflush=False, expire_on_commit=False):
    try:
        return _configure_session(_ro_session_factory, autocommit, autoflush, expire_on_commit)
    except Exception as exc:
        raise(exc)


def create_session(autocommit=False, autoflush=False, expire_on_commit=True):
    try:
        return _configure_session(_session_factory, autocommit, autoflush, expire_on_commit)
    except Exception as exc:
        raise(exc)

# References
#
#   http://docs.sqlalchemy.org/en/latest/core/engines.html#sqlalchemy.create_engine
#   http://docs.sqlalchemy.org/en/latest/core/pooling.html
#   http://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.Connection
#   http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session.__init__
