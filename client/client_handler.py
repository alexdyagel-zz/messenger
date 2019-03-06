import threading
import socket


class Client:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self, ip, port):
        self.sock.connect((ip, port))
        threading.Thread(target=self.receive_data()).start()

    def receive_data(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            print(data.decode("utf-8"))

    def sign_in_to_server(self):
        self.sock.send(bytes(input(""), "utf-8"))

    def send_msg(self):
        while True:
            self.sock.send(bytes(input(""), "utf-8"))
