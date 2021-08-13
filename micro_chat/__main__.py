import argparse

from . import config, Server, Client

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--server', help=f'Run a {config.PROGRAM_NAME} server',
    action='store_true')
parser.add_argument('-c', '--client', help=f'Run a {config.PROGRAM_NAME} client ' + 
    'and connect to a server', action='store_true')

args = parser.parse_args()

if args.server:
    Server().run()
elif args.client:
    Client().run()
else:
    parser.print_usage()
    quit()