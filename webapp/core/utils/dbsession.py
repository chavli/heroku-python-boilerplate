"""
    sqlalchemy database session manager. this code is based on the advice from these pages:

    https://docs.sqlalchemy.org/en/latest/orm/session_basics.html
    https://docs.sqlalchemy.org/en/latest/orm/contextual.html
    http://stackoverflow.com/questions/12223335/sqlalchemy-creating-vs-reusing-a-session
    http://stackoverflow.com/questions/5544774/whats-the-recommended-scoped-session-usage-pattern-in-a-multithreaded-sqlalchem
"""
from . import create_read_session, create_session
from contextlib import contextmanager


@contextmanager
def dbsession():
    session = None
    try:
        session = create_session(autocommit=False, autoflush=False, expire_on_commit=True)
        yield session
        session.commit()
    except Exception as exc:
        if session:
            session.rollback()
        raise(exc)
    finally:
        if session:
            session.close()


@contextmanager
def read_dbsession():
    session = None
    try:
        session = create_read_session(autocommit=False, autoflush=False, expire_on_commit=False)
        yield session
        session.commit()
    except Exception as e:
        if session:
            session.rollback()
        raise(e)
    finally:
        if session:
            session.close()
