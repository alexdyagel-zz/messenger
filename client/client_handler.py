import pickle
import socket
import threading

CODING = "utf-8"
QUIT = "[quit]"


class Client:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self, ip, port, login, password):
        self.connect_to_server(ip, port)
        if not self.authorize(login, password):
            raise Exception("Invalid password")
        else:
            threading.Thread(target=self.receive_data).start()
            threading.Thread(target=self.send_msg).start()

    def connect_to_server(self, ip, port):
        self.sock.connect((ip, port))

    def authorize(self, login, password):
        credentials = pickle.dumps((login, password))
        self.sock.send(credentials)
        response = self.sock.recv(4096)
        response = pickle.loads(response)
        return response

    def receive_data(self):
        while True:
            data = self.sock.recv(1024)
            data = data.decode(CODING)
            if data != QUIT:
                print(data)
            else:
                raise SystemExit

    def send_msg(self):
        while True:
            self.sock.send(input("").encode(CODING))

    def communicate_with_server(self):
        pass
