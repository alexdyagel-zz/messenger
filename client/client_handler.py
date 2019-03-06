import pickle
import socket
import threading


class Client:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self, ip, port, login, password):
        self.sock.connect((ip, port))
        if not self.authorize(login, password):
            raise Exception("Invalid password")
        else:
            threading.Thread(target=self.receive_data).start()
            threading.Thread(target=self.send_msg()).start()

    def authorize(self, login, password):
        credentials = pickle.dumps((login, password))
        self.sock.send(credentials)
        response = self.sock.recv(4096)
        response = pickle.loads(response)
        return response

    def receive_data(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            print(data.decode("utf-8"))

    def send_msg(self):
        while True:
            self.sock.send(bytes(input(""), "utf-8"))
