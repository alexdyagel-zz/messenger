from handler import arguments_validation
from handler.server_handler import Server

if __name__ == "__main__":
    args = arguments_validation.init_args()
    server = Server(args.port)
    server.run()
