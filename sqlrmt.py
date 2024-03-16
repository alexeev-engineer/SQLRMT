#!/usr/bin/python3
"""SQLRMT
Software for working with remote SQL databases via the network.
SQLRMT is asynchronous, uses network traffic protection mechanisms and is extensible
SQLRMT - blazing fast tool for work with remote databases.

Copyright © 2024 Alexeev Bronislav. All rights reversed
"""
import argparse
import signal
import sys
from functools import cache
from pathlib import Path
from time import monotonic
from rich import print
from configparser import ConfigParser
import asyncio

from modules.server.server import Server
from modules.client.client import Client
from modules.logger import log

__version__ = '0.1.0'
__author__ = 'Alexeev Bronislav'


def signal_handler(signal, frame):
	log('Shutdown SQLRMT...', 'warn')
	sys.exit(0)


@cache
async def main():
	"""Main function."""
	print(f'SQLRMT {__version__} @ {__author__}')
	print('Run with `--help` flag to view help\n')
	signal.signal(signal.SIGINT, signal_handler)

	parser = argparse.ArgumentParser(description='Software for working with remote SQL databases via the network')
	parser.add_argument("-s", "--server", action="store_true", help='Start server')
	parser.add_argument("-c", "--client", action="store_true", help='Start client')
	parser.add_argument('--host', type=str, help='Server hostname')
	parser.add_argument('-p', '--port', type=str, help='Server port')
	parser.add_argument('-d', '--database', type=str, help='Database file name')
	parser.add_argument('-t', '--timeout', type=str, help='Client timeout')
	parser.add_argument("--server-cert", type=str, help='Server certificate file')
	parser.add_argument("--client-cert", type=str, help='Client certificate file')
	parser.add_argument("--server-key", type=str, help='Server secure key file')
	parser.add_argument("--client-key", type=str, help='Client secure key file')
	parser.add_argument("--config", default='config.ini', help='Configuration file')

	args = parser.parse_args()

	config_path = Path(args.config)

	if config_path.exists():
		config = ConfigParser()
		config.read(args.config)
		server_host = config.get('Server', 'host')
		server_port = config.get('Server', 'port')
		server_db = config.get('Server', 'database')
		client_timeout = config.get('Client', 'timeout')

		if args.host:
			server_host = args.host
		elif args.port:
			server_port = args.port
		elif args.timeout:
			client_timeout = args.timeout
		elif args.database:
			server_db = args.database

		if args.server and args.client_cert and args.server_key and args.server_cert:
			print('[green]Starting the server...[/green]')
			server = Server(server_host, int(server_port), args.client_cert, args.server_key, args.server_cert)
			
			start = monotonic()
			task = asyncio.create_task(server.listen())
			await task
			end = monotonic()

			total = round(end - start, 3)
			print(f'\nConnection uptime: {total} sec.')
		elif args.client and args.client_key and args.client_cert and args.server_cert:
			print('[green]Starting the client...[/green]')
			client = Client(server_host, int(server_port), int(client_timeout), args.client_key, args.client_cert, args.server_cert)

			start = monotonic()
			task = asyncio.create_task(client.connect())
			await task
			end = monotonic()

			total = round(end - start, 3)
			print(f'\nConnection uptime: {total} sec.')
	else:
		print(f'[red]Error: config file "{args.config}" don\'t exists[/red]')


if __name__ == '__main__':
	"""Run tasks"""
	asyncio.run(main())
