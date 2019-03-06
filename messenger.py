from client import actions, client_handler
from client.client_handler import *

if __name__ == "__main__":
    args = actions.init_args()
    client = Client()
    client.connect_to_server(args.ip, args.port)
