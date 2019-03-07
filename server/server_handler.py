import pickle
import socket
from threading import Thread

from server.model.database import DatabaseHandler, User

CODING = "utf-8"
QUIT = "[quit]"


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

    def send(self, data):
        self.sock.send(data)

    def close_socket(self):
        self.sock.close()


class Server(metaclass=MetaSingleton):
    DEFAULT_PORT = 8080
    BUFSIZE = 1024

    def __init__(self, ip, port):
        ip = socket.gethostbyname(socket.gethostname()) if ip is None else ip
        port = Server.DEFAULT_PORT if port is None else port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        self.server.listen(1)
        self.clients = []

    def run(self):
        while True:
            client_sock, client_address = self.server.accept()
            ip, port = client_address
            print("{}:{} has connected.".format(ip, port))
            client = Client(client_sock, ip, port)
            Thread(target=self.handle_new_connection, args=(client,)).start()

    def handle_new_connection(self, client):
        login, password = pickle.loads(client.sock.recv(1024))
        user = User(login, password)
        if Server.authorize(user):
            client.send(pickle.dumps(True))
            client.login = login
            self.welcome_new_client(client)
            self.clients.append(client)
            self.communicate_with_client(client)
        else:
            client.send(pickle.dumps(False))
            return

    def welcome_new_client(self, client):
        welcome = 'Welcome {}! If you ever want to quit, type [quit] to exit.'.format(client.login)
        client.send(welcome.encode(CODING))
        msg = "{} has joined the chat!".format(client.login)
        self.broadcast(msg.encode(CODING), client)

    def communicate_with_client(self, client):
        while True:
            msg = client.sock.recv(self.BUFSIZE)
            msg = msg.decode(CODING)
            if msg != QUIT:
                self.broadcast("[{}]: {}".format(client.login, msg).encode(CODING), client)
            else:
                client.send(QUIT.encode(CODING))
                client.close_socket()
                print("{}:{} [{}] disconnected.".format(client.ip, client.port, client.login))
                self.clients.remove(client)
                self.broadcast("{} has left the chat.".format(client.login).encode(CODING))
                break

    @staticmethod
    def authorize(user):
        messenger_db = DatabaseHandler("sqlite:///messengerDB")
        found_user = messenger_db.get_by_login(user.login)
        if found_user is not None:
            if found_user.password == user.password:
                return True
            else:
                return False
        else:
            messenger_db.add(user)
            return True

    def broadcast(self, msg, sender=None):
        for client in self.clients:
            if client is not sender:
                client.send(msg)
