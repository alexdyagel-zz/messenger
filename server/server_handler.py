import threading
import socket
from threading import Thread


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Server(metaclass=MetaSingleton):
    DEFAULT_PORT = 8080
    BUFSIZE = 1024

    def __init__(self, ip, port):
        ip = socket.gethostbyname(socket.gethostname()) if ip is None else ip
        port = Server.DEFAULT_PORT if port is None else port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        self.server.listen(1)
        self.addresses = {}
        self.clients = {}

    def run(self):
        while True:
            client, client_address = self.server.accept()
            ip, port = client_address
            print("{}:{} has connected.".format(ip, port))
            client.send(bytes("Connection with server is successful!", "utf8"))
            self.addresses[client] = client_address
            Thread(target=self.handle, args=(client, client_address)).start()

    def handle(self, client, client_address):
        name = client.recv(self.BUFSIZE).decode("utf8")
        welcome = 'Welcome {}! If you ever want to quit, type [quit] to exit.'.format(name)
        client.send(bytes(welcome, "utf8"))
        msg = "{} has joined the chat!".format(name)
        self.broadcast(bytes(msg, "utf8"))
        self.clients[client] = name
        ip, port = client_address
        while True:
            msg = client.recv(self.BUFSIZE)
            if msg != bytes("[quit]", "utf8"):
                self.broadcast(msg, name + ": ")
            else:
                client.send(bytes("[quit]", "utf8"))
                client.close()
                print("{}:{} [{}] disconnected.".format(ip, port, name))
                self.clients.pop(client)
                self.broadcast(bytes("{} has left the chat.".format(name), "utf8"))
                break

    def broadcast(self, msg, prefix=""):  # prefix is for name identification.
        for sock in self.clients:
            sock.send(bytes(prefix, "utf8") + msg)
