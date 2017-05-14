"""
    sqlalchemy database session manager. this code is based on the advice from these pages:

    https://docs.sqlalchemy.org/en/latest/orm/session_basics.html
    https://docs.sqlalchemy.org/en/latest/orm/contextual.html
    http://stackoverflow.com/questions/12223335/sqlalchemy-creating-vs-reusing-a-session
    http://stackoverflow.com/questions/5544774/whats-the-recommended-scoped-session-usage-pattern-in-a-multithreaded-sqlalchem
"""
from contextlib import contextmanager
from sqlalchemy.orm import scoped_session


@contextmanager
def dbsession():
    try:
        session = scoped_session(Session)
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise(e)
    finally:
        session.close()
