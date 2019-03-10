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
db_dir = os.path.join(package_directory, 'model', 'messengerDB')
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
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Client:
    def __init__(self, sock, ip, port, login=None):
        self.sock = sock
        self.ip = ip
        self.port = port
        self.login = login
        self.salt = None

    def __str__(self):
        return self.login

    def send(self, data):
        self.sock.send(data)

    def accept(self):
        return self.sock.recv(BUFSIZE)

    def close_socket(self):
        self.sock.close()


class Server(metaclass=MetaSingleton):
    DEFAULT_PORT = 8080

    def __init__(self, ip, port):
        ip = socket.gethostbyname(socket.gethostname()) if ip is None else ip
        port = Server.DEFAULT_PORT if port is None else port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        self.server.listen(1)
        self.clients = []
        self.connections = [self.server]

    def run(self):
        logger.info("Running server")
        while True:
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
                            self.handle(client)
                            break

    def validate_credentials(self, client):
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
            return

    @staticmethod
    def hash_password(password):
        return hashpw(password.encode(CODING), SALT)

    def welcome_new_client(self, client):
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

    def handle(self, client):
        try:
            msg = client.accept()
        except:
            self.broadcast("{} has left the chat.".format(client.login).encode(CODING))
            print("{}:{} [{}] disconnected.".format(client.ip, client.port, client.login))
            client.close_socket()
            self.connections.remove(client.sock)
            return

        if msg:
            msg = msg.decode(CODING)
            if msg != QUIT:
                self.route_msg(msg, client)
            else:
                client.close_socket()
                print("{}:{} [{}] disconnected.".format(client.ip, client.port, client.login))
                self.clients.remove(client)
                self.connections.remove(client.sock)
                self.broadcast("{} has left the chat.".format(client.login).encode(CODING))

    @staticmethod
    def authorize(user):
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
        for client in self.clients:
            if client is not sender:
                client.send(msg)

    def route_msg(self, msg, sender):
        tag = TAG.match(msg)
        if tag is not None:
            receiver_login = tag.group(1)[1:]
            receiver = self.get_user_by_login(receiver_login)
            msg = " ".join(msg.split()[1:])
            if receiver is not None:
                receiver.send("[{}]: {}".format(sender.login, msg).encode(CODING))
        else:
            self.broadcast("[{}]: {}".format(sender.login, msg).encode(CODING), sender)

    def get_user_by_login(self, login):
        for client in self.clients:
            if client.login == login:
                return client
        return None
