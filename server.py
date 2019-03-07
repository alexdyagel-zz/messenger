from server import arguments_validation
from server.server_handler import Server

if __name__ == "__main__":
    args = arguments_validation.init_args()
    server = Server(args.ip, args.port)
    server.run()
