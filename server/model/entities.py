from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Route(Base):
    __tablename__ = 'route'
    message_id = Column(
        Integer,
        ForeignKey('message.id'),
        primary_key=True)

    receiver_login = Column(
        String,
        ForeignKey('user.login'),
        primary_key=True)


class User(Base):
    __tablename__ = 'user'
    login = Column(String, primary_key=True)
    password = Column(String)

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __repr__(self):
        return self.login


class Message(Base):
    __tablename__ = 'message'
    id = Column(String, primary_key=True)
    content = Column(String)
    sender_login = Column(String, ForeignKey('user.login'))
    sender = relationship("User")
    receivers = relationship(User, secondary='route')

    def __init__(self, id_, content, sender_login, receiver_login):
        self.id = id_
        self.content = content
        self.sender_login = sender_login
        self.receiver_login = receiver_login

    def __repr__(self):
        return """
        From: {}
        To: {}
        Message:
        {}    """.format(self.sender_login, self.receiver_login, self.content)
