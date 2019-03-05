from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


@contextmanager
def db_session(db_url):
    """
    Creates a context with an open SQLAlchemy session.
    """
    engine = create_engine(db_url, convert_unicode=True)
    connection = engine.connect()
    session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine, expire_on_commit=False))
    try:
        yield session
    finally:
        session.commit()
        session.expunge_all()
        session.close()
        connection.close()


class DatabaseHandler(object):
    def __init__(self, database_url):
        self.database_url = database_url

    def get_all(self, entity_type):
        with db_session(self.database_url) as db:
            all_values = db.query(entity_type.value).all()
        return all_values

    def add(self, entity):
        with db_session(self.database_url) as db:
            db.add(entity)
