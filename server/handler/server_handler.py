import logging
import os
import pickle
import re
import select
import socket
import sys

from bcrypt import hashpw

from server.model.database import DatabaseHandler, User

SALT = b'$2b$12$D39eUP1wg.Z.SVR4SfhLxu'
CODING = "utf-8"
QUIT = "[quit]"
TAG = re.compile("(@[^\s]+)")
BUFSIZE = 4096

package_directory = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(package_directory, '..', 'model', 'messengerDB')
MESSENGER_DB = ''.join(['sqlite:///', db_dir])

logger = logging.getLogger(__name__)
logfile = "messenger_server_log.log"

formatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')

file_handler = logging.FileHandler(logfile)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

screen_handler = logging.StreamHandler(sys.stdout)
screen_handler.setLevel(logging.INFO)
screen_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(screen_handler)
logger.setLevel(logging.DEBUG)


class MetaSingleton(type):
    """
          Metaclass for implementation of singleton pattern.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Client:
    """
        This is a class for making clients entities and interacting with clients sockets.

        Attributes:
            sock (socket.socket): Clients socket.
            ip (str): Clients ip address.
            port (int): Clients port.
            login (str): Clients login.
    """

    def __init__(self, sock, ip, port, login=None):
        self.sock = sock
        self.ip = ip
        self.port = port
        self.login = login

    def __str__(self):
        return self.login

    def send(self, data):
        """
        Sends data through socket
        :param data: encoded data
        """
        self.sock.send(data)

    def accept(self):
        """
        Accepts data from socket
        :return: binary data
        """
        return self.sock.recv(BUFSIZE)

    def close_socket(self):
        """
        closes socket
        """
        self.sock.close()


class Server(metaclass=MetaSingleton):
    """
            This is a class for interacting with clients. This class uses singleton pattern

            Attributes:
                server (socket.socket): Servers socket.
                clients (list): List of Client objects.
                connections (list): List of socket.socket objects with connections to read.
    """

    DEFAULT_PORT = 8080

    def __init__(self, port):
        ip = socket.gethostbyname(socket.gethostname())
        port = Server.DEFAULT_PORT if port is None else port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        self.server.listen(1)
        self.clients = []
        self.connections = [self.server]

    def run(self):
        """
        Runs server for handling connections
        """
        logger.info("Running server")
        while True:
            self.handle_connections()

    def handle_connections(self):
        """
        Handles connections from the connections list. Uses select module for asynchronous interaction.
        If connection is server socket, then it accepts new connection and calls method for validating clients
        credentials. Else it handles client by calling method for it.
        """
        read_sockets, write_sockets, error_sockets = select.select(self.connections, [], [])
        for sock in read_sockets:
            if sock == self.server:
                client_sock, (ip, port) = self.server.accept()
                self.connections.append(client_sock)
                logger.info("{}:{} has connected.".format(ip, port))
                client = Client(client_sock, ip, port)
                self.validate_credentials(client)
            else:
                for client in self.clients:
                    if client.sock == sock:
                        self.handle_client(client)
                        break

    def validate_credentials(self, client):
        """
        Validates users credentials.
        It accepts credentials, creates User object and check for authorization using authorize method.
        In case of successful authorization it send boolean True response and welcome message to user and adds it to
        list of clients. In case of unsuccessful authorization it sends boolean False response and removes clients
        connection from list
        :param client: Client object
        """
        login, password = pickle.loads(client.accept())
        hashed_password = self.hash_password(password)
        user = User(login, hashed_password)
        if Server.authorize(user):
            client.send(pickle.dumps(True))
            client.login = login
            self.welcome_new_client(client)
            self.clients.append(client)
        else:
            client.send(pickle.dumps(False))
            self.connections.remove(client.sock)

    @staticmethod
    def hash_password(password):
        """
        Hash password with the help of hashpw method of bcrypt module
        :param password: users password
        :return: hashed password
        """
        return hashpw(password.encode(CODING), SALT)

    def welcome_new_client(self, client):
        """
        Generates welcome message and sends it to client.
        Notifies other users about connected user.
        :param client:
        """
        welcome = " =========================================================================="
        welcome += "\n|| Welcome {}!".format(client.login)
        welcome += "\n|| If you ever want to quit, type [quit] to exit."
        welcome += "\n|| By default you send broadcast messages"
        welcome += "\n|| To address certain user use this template: @user_login message"
        if len(self.clients) != 0:
            welcome += "\n|| Available users: "
            for user in self.clients:
                welcome += "\n||   {}".format(user.login)
        welcome += " \n==========================================================================\n"

        client.send(welcome.encode(CODING))
        msg = "[{}] ==> joined the chat!".format(client.login)
        self.broadcast(msg.encode(CODING), client)

    def handle_client(self, client):
        """
        Tries to accept message from user, in case of exception or QUIT message from user removes client from chat.
        :param client: Client object
        """
        try:
            msg = client.accept()
        except socket.error or socket.timeout:
            self.remove_client_from_chat(client)
            return

        if msg:
            msg = msg.decode(CODING)
            if msg != QUIT:
                self.route_msg(msg, client)
            else:
                self.remove_client_from_chat(client)

    def remove_client_from_chat(self, client):
        """
        Closes clients socket remove it from connections list and clients list. Notifies other users about leaving this
        user from chat.
        :param client: Client object
        """
        client.close_socket()
        logger.info("{}:{} [{}] disconnected.".format(client.ip, client.port, client.login))
        self.clients.remove(client)
        self.connections.remove(client.sock)
        self.broadcast("[{}] <== left the chat.".format(client.login).encode(CODING))

    @staticmethod
    def authorize(user):
        """
        Checks for user login in database, if it is found, check the equality of hashed passwords.
        If login is not found, adds user to database.
        :param user: User object
        :return: response about authorization result
        """
        messenger_db = DatabaseHandler(MESSENGER_DB)
        found_user = messenger_db.get_by_login(user.login)
        if found_user is not None:
            if user.password == found_user.password:
                logger.info("User {} successfully signed in".format(user.login))
                return True
            else:
                logger.info("Authorization failed for user {}. Incorrect password.".format(user.login))
                return False
        else:
            messenger_db.add(user)
            logger.info("User {} successfully signed up".format(user.login))
            return True

    def broadcast(self, msg, sender=None):
        """
        Sends broadcast message to all available clients except sender (if it is specified).
        :param msg: message to be sent
        :param sender: Client object, which sent message
        """
        for client in self.clients:
            if client is not sender:
                client.send(msg)

    def route_msg(self, msg, sender):
        """
        Routes message from user. Checks for tag @ in message for routing to tagged user.
        :param msg: message to be sent
        :param sender: Client object, which sent message
        """
        tag = TAG.match(msg)
        if tag is not None:
            receiver_login = tag.group(1)[1:]
            receiver = self.find_client_by_login(receiver_login)
            msg = " ".join(msg.split()[1:])
            if receiver is not None:
                receiver.send("[{}]: {}".format(sender.login, msg).encode(CODING))
        else:
            self.broadcast("[{}]: {}".format(sender.login, msg).encode(CODING), sender)

    def find_client_by_login(self, login):
        """
        Finds client in list by login
        :param login: clients login
        :return: Client object if there is client with given login, else None
        """
        for client in self.clients:
            if client.login == login:
                return client
        return None
