from client.handler import arguments_validation
from client.handler.client_handler import *

if __name__ == "__main__":
    args = arguments_validation.init_args()
    client = Client()
    client.run(args.ip, args.port, args.login, args.password)
