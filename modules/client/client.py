#!/usr/bin/python3
"""SQLRMT
Software for working with remote SQL databases via the network.
SQLRMT is asynchronous, uses network traffic protection mechanisms and is extensible
SQLRMT - blazing fast tool for work with remote databases.

Copyright © 2024 Alexeev Bronislav. All rights reversed
"""
import socket
import ssl
import asyncio
from functools import cache
from rich import print


class Client:
	"""TLS-Client class

	Arguments:
	---------
	 + 

	"""

	def __init__(self, host: str, port: int, timeout: int, client_key: str, client_cert: str, server_cert: str):
		self.host: str = host
		self.port: int = port
		self.timeout: int = timeout
		self.client_key: str = client_key
		self.client_cert: str = client_cert
		self.server_cert: str = server_cert

		print('[blue]Create SSL context for client[/blue]')
		self.context = ssl.SSLContext(ssl.PROTOCOL_TLS, cafile=self.server_cert)
		self.context.load_cert_chain(certfile=self.client_cert, keyfile=self.client_key)
		self.context.load_verify_locations(cafile=self.server_cert)
		self.context.verify_mode = ssl.CERT_REQUIRED
		self.context.options |= ssl.OP_SINGLE_ECDH_USE
		self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2

		print('[blue]Create client socket[/blue]')
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		self.client.settimeout(self.timeout)

	@cache
	async def broadcast(self, socks):
		while True:
			message = input("SQLRMT > ")

			if message == 'help':
				print(f'''Help for SQLRMT Client

	help - view help
	disconnect/exit/quit - disconnect from server

Currently connected to {self.host}:{self.port}''')
			elif message in ['disconnect', 'exit', 'quit']:
				socks.send(b'DISCONNECT')
				exit()
			elif len(message) > 0:
				socks.send(message.encode())
				receives = socks.recv(1024)
				print(f'[blue]SERVER[/blue] -- [bold]{receives.decode()}[/bold]')

	@cache
	async def connect(self):
		print(f'[blue]Connect to {self.host}:{self.port}[/blue]')

		try:
			self.client.connect((self.host, self.port))

			with self.context.wrap_socket(self.client, server_side=False, server_hostname=self.host) as socks:
				print(f'[cyan]TLS Version: {socks.version()}[/cyan]')
				print('[cyan]Enter `help` for view help[/cyan]\n')
			
				task = asyncio.create_task(self.broadcast(socks))
				await task
		except TimeoutError:
			print('[red]The server is busy. Connect later[/red]')
			self.client.close()
			exit()
