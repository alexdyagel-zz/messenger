from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from .entities import *


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


class DatabaseHandler:
    """
           This is a class for making operations with database.

           Attributes:
               database_url (str): Url address of databse.
    """

    def __init__(self, database_url):
        self.database_url = database_url

    def get_by_login(self, login):
        """
        Get User object from database by login of user.
        :param login: users login
        :return: User object or None if user not found
        """
        with db_session(self.database_url) as db:
            value = db.query(User).filter_by(login=login).first()
        return value

    def add(self, user):
        """
        Adds User object to database
        :param user: User object
        """
        with db_session(self.database_url) as db:
            db.add(user)
