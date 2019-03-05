import argparse


def init_args():
    """
    Initializes commandline arguments. Defines expected arguments. May cause parser errors in case of wrong arguments.
    :return: parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='This is a server for messenger')

    parser.add_argument('--ip',
                        type=str,
                        help='Optional str argument with ip address of the server',
                        required=True)

    parser.add_argument('--port',
                        type=int,
                        help='Optional int argument with port of server',
                        required=True)

    args = parser.parse_args()
    validate_args(args, parser)
    return args


def validate_args(args, parser):
    pass
