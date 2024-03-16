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

from modules.logger import log
from modules.server.database import validate


class Client:
	"""TLS-Client class.

	Arguments:
	---------
	 + host: str

	"""

	def __init__(self, host: str, port: int, timeout: int, client_key: str, client_cert: str, server_cert: str):
		self.host: str = host
		self.port: int = port
		self.timeout: int = timeout
		self.client_key: str = client_key
		self.client_cert: str = client_cert
		self.server_cert: str = server_cert

		log('Create SSL context for client', 'debug')
		# create ssl context
		self.context = ssl.SSLContext(ssl.PROTOCOL_TLS, cafile=self.server_cert)
		self.context.load_cert_chain(certfile=self.client_cert, keyfile=self.client_key)
		self.context.load_verify_locations(cafile=self.server_cert)
		self.context.verify_mode = ssl.CERT_REQUIRED
		self.context.options |= ssl.OP_SINGLE_ECDH_USE
		self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2

		log('Create client socket', 'debug')
		# create socket
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		self.client.settimeout(self.timeout)

	@cache
	async def broadcast(self, socks):
		"""Broadcast function: receives and sends messages.

		Arguments:
		---------
		+ socks - the socket ssl wrapper

		"""
		while True:
			# receive and send messages
			message = input('SQLRMT query> ')
			
			try:
				if message == 'help':
					log(f'''Help for SQLRMT Client

		help - view help
		disconnect/quit/exit - disconnect from server

	Currently connected to {self.host}:{self.port}''', 'none')
				elif message in ['disconnect', 'quit', 'exit']:
					log('Disconnect from server...', 'debug')
					try:
						socks.send(b'DISCONNECT')
					except ssl.SSLError as ex:
						log(f"An error occurred on the client side while sending a request to the server: {ex}", 'error')

					exit()
				elif len(message) > 0:
					if validate(message):
						socks.send(message.encode())
						receives = socks.recv(1024)
						log(f'[bold]{receives.decode()}[/bold]', 'SERVER')
			except ssl.SSLError as ex:
				log(f"An error occurred on the client side while sending a request to the server: {ex}", 'error')

	@cache
	async def connect(self):
		"""Connect to server."""
		log(f'[blue]Connect to {self.host}:{self.port}[/blue]')

		# connect to server and start broadcast
		try:
			self.client.connect((self.host, self.port))

			with self.context.wrap_socket(self.client, server_side=False, server_hostname=self.host) as socks:
				log(f'TLS Version: {socks.version()}', 'debug')
				log('Enter `help` for view help\n', 'none')
			
				task = asyncio.create_task(self.broadcast(socks))
				await task
		except TimeoutError:
			log('The server is busy (timeout error). Connect later', 'red')
			self.client.close()
			exit()
		except ConnectionRefusedError:
			log('Check if you are connected to the network (if the server is not on local network) and if the server is turned on.', 'error')
