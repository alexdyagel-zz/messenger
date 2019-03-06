# import enum
# import pickle
# from abc import ABCMeta, abstractmethod
#
# from server.model.database import *
#
#
# class Command(metaclass=ABCMeta):
#     @abstractmethod
#     def execute(self):
#         pass
#
#
# class Authorize(Command):
#     def __init__(self, client):
#         self.client = client
#
#     def execute(self):
#         login, password = pickle.load(self.client.recv(1024))
#         messenger_db = DatabaseHandler("sqlite:///messengerDB")
#         user = messenger_db.get_by_login(login)
#         if user is not None:
#             if user.password == password:
#                 self.client.send(pickle.dumps(True))
#             else:
#                 self.client.send(pickle.dumps(False))
#         else:
#             messenger_db.add(User(login, password))
#
#
# class SendMessageCommand(Command):
#     def __init__(self, client):
#         self.client = client
#
#     def execute(self):
#         pass
#
#
# class SendBroadcastMessageCommand(Command):
#     def __init__(self, client):
#         self.client = client
#
#     def execute(self):
#         pass
#
#
# @enum.unique
# class CommandType(enum.Enum):
#     AUTHORIZE = 0
#     SEND_MSG = 2
#     SEND_BROADCAST_MSG = 3
#
#
# commands = {CommandType.AUTHORIZE: Authorize,
#             CommandType.SEND_MSG: SendMessageCommand,
#             CommandType.SEND_BROADCAST_MSG: SendBroadcastMessageCommand}
