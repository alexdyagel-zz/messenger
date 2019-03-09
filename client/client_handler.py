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
            threading.Thread(target=self.send_data).start()
            threading.Thread(target=self.receive_data).start()

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
            try:
                received_data = self.accept_msg()
            except:
                print("Server closed connection.")
                break
            if not received_data:
                print("Server closed connection.")
                break
            else:
                print("Received data: {}".format(received_data.decode(CODING)))

    def send_data(self):
        while True:
            send_data = input("")
            if send_data == QUIT:
                self.send(send_data.encode(CODING))
                break
            else:
                self.send(send_data.encode(CODING))
