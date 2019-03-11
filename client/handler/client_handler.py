import pickle
import socket
import threading

CODING = "utf-8"
QUIT = "[quit]"
BUFSIZE = 4096


class Client:
    """
            This is a class for interacting with server.

            Attributes:
                sock (socket.socket): Clients socket.
    """

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self, ip, port, login, password):
        """
        Running client.
        Connects to server. Checks authorization and start threads for sending data and receiving data.
        :param ip: ipv4 address of server
        :param port: port of server
        :param login: login of user
        :param password: password of user
        """

        try:
            self.connect_to_server(ip, port)
        except socket.error:
            print("Unable to connect to server")
            raise
        else:
            if not self.authorize(login, password):
                raise Exception("Invalid password")
            else:
                send_thread = threading.Thread(target=self.send_data)
                send_thread.setDaemon(True)
                send_thread.start()
                threading.Thread(target=self.receive_data).start()

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

    def connect_to_server(self, ip, port):
        """
        Connects to server
        :param ip: ip address of server
        :param port: port of server
        """
        self.sock.connect((ip, port))

    def authorize(self, login, password):
        """
        Sends credentials to server and checks response.
        :param login: users login
        :param password: users password
        :return: boolean response
        """
        credentials = pickle.dumps((login, password))
        self.send(credentials)
        response = self.accept()
        response = pickle.loads(response)
        return response

    def receive_data(self):
        """
        In infinity loop receives data from server and prints it.
        """
        while True:
            try:
                received_data = self.accept()
            except socket.error or socket.timeout:
                print("Server closed connection.")
                break
            if not received_data:
                print("Server closed connection.")
                break
            else:
                print(received_data.decode(CODING))

    def send_data(self):
        """
        In infinity loop waits for entering data in prompt and sends it to server.
        """
        while True:
            send_data = input("")
            if send_data == QUIT:
                self.send(send_data.encode(CODING))
                break
            else:
                self.send(send_data.encode(CODING))
