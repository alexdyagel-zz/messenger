from server import actions
from server.server_handler import Server

if __name__ == "__main__":
    args = actions.init_args()
    server = Server(args.ip, args.port)
    server.run()
