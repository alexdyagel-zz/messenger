from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
            This is a class for mapping entities from database to python objects.

            Attributes:
                login (str): users login.
                password (str): users hashed password.
    """

    __tablename__ = 'user'
    login = Column(String, primary_key=True)
    password = Column(String)

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __repr__(self):
        return self.login
