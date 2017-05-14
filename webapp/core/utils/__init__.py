import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if "DATABASE_URL" in os.environ:
    _engine = create_engine(os.getenv("DATABASE_URL"), convert_unicode=True)
    Session = sessionmaker()

    # http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session.__init__
    Session.configure(autocommit=False, autoflush=False, expire_on_commit=True, bind=_engine)
else:
    print("Utils running without database")
