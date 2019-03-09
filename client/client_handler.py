import pickle
import socket
import threading

CODING = "utf-8"
QUIT = "[quit]"
BUFSIZE = 4096


class Client:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self, ip, port, login, password):
        self.connect_to_server(ip, port)
        if not self.authorize(login, password):
            raise Exception("Invalid password")
        else:
            threading.Thread(target=self.communicate).start()
            self.receive_data()

    def send(self, data):
        self.sock.send(data)

    def accept_msg(self):
        return self.sock.recv(BUFSIZE)

    def close_socket(self):
        self.sock.close()

    def connect_to_server(self, ip, port):
        self.sock.connect((ip, port))

    def authorize(self, login, password):
        credentials = pickle.dumps((login, password))
        self.send(credentials)
        response = self.accept_msg()
        response = pickle.loads(response)
        return response

    def receive_data(self):
        while True:
            data = self.accept_msg()
            data = data.decode(CODING)
            if data != QUIT:
                print(data)
            else:
                raise SystemExit

    def communicate(self):
        while True:
            self.send(input("").encode(CODING))
