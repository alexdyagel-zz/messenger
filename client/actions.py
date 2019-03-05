import argparse


def init_args():
    """
    Initializes commandline arguments. Defines expected arguments. May cause parser errors in case of wrong arguments.
    :return: parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='This is a great messenger which allows you to communicate with your friends through commandline')

    required = parser.add_argument_group('required arguments')

    required.add_argument('--ip',
                          type=str,
                          help='Str argument with ip address of the server',
                          required=True)

    required.add_argument('--port',
                          type=int,
                          help='Int argument with port of server',
                          required=True)

    required.add_argument('--login',
                          type=str,
                          help='Str argument with user login',
                          required=True)

    required.add_argument('--password',
                          type=str,
                          help='Str argument with password of your account',
                          required=True)

    args = parser.parse_args()
    validate_args(args, parser)
    return args


def validate_args(args, parser):
    pass
