#!/usr/bin/python3
"""SQLRMT
Software for working with remote SQL databases via the network.
SQLRMT is asynchronous, uses network traffic protection mechanisms and is extensible
SQLRMT - blazing fast tool for work with remote databases.

Copyright © 2024 Alexeev Bronislav. All rights reversed
"""
import readline # !!! DON'T DELETE THIS IMPORT !!!
import socket
import ssl
import asyncio

from modules.logger import log


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

	async def broadcast(self, socks):
		"""Broadcast function: receives and sends messages.

		Arguments:
		---------
		+ socks - the socket ssl wrapper

		"""
		attempts = 0
		while True:
			if attempts > 2:
				log('Verification passed. Successful connection to the database. Exit...', 'exception')
				socks.send(b'DISCONNECT')
				exit()

			passphrase = input('Enter the password to connect to the database: ')

			if len(passphrase) > 0:
				attempts += 1
				socks.send(passphrase.encode())
				resp = socks.recv(1024).decode()

				if resp == 'SUCCESS':
					log('Verification passed. Successful connection to the database, welcome!', 'info')
					break
				else:
					log('Verification failed. Please try another passphrase.', 'error')

		while True:
			# receive and send messages
			try:
				message = input('SQLRMT query> ')
			except KeyboardInterrupt:
				print()
				continue
			
			try:
				if message == 'help':
					log(f'''Help for SQLRMT Client

		help - view help
		disconnect/quit/exit - disconnect from server
		connect <database> - connect to new database
		info - info about connection

Currently connected to {self.host}:{self.port}''', 'none')
				elif message in ['disconnect', 'quit', 'exit']:
					log('Disconnect from server...', 'debug')
					try:
						socks.send(b'DISCONNECT')
					except ssl.SSLError as ex:
						log(f"An error occurred on the client side while sending a request to the server: {ex}", 'error')

					exit()
				elif message.split(' ')[0] == 'connect':
					database = message.split(' ')[1]

					if database:
						socks.send(f'RECONNECT {database}'.encode())
						receives = socks.recv(1024)
						log(f'{receives.decode()}', 'SERVER')
				elif message == 'info':
					socks.send(b'INFO')
					receives = socks.recv(1024)
					log(f'{receives.decode()}', 'SERVER')
				elif len(message) > 0:
					socks.send(message.encode())
					receives = socks.recv(1024)
					log(f'{receives.decode()}', 'SERVER')
			except ssl.SSLError as ex:
				log(f"An error occurred on the client side while sending a request to the server: {ex}", 'error')

	async def connect(self):
		"""Connect to server."""
		log(f'Connect to {self.host}:{self.port}')

		# connect to server and start broadcast
		try:
			self.client.connect((self.host, self.port))

			with self.context.wrap_socket(self.client, server_side=False, server_hostname=self.host) as socks:
				log(f'TLS Version: {socks.version()}', 'debug')
				log('Enter `help` for view help\n', 'none')
			
				task = asyncio.create_task(self.broadcast(socks))
				await task
		except TimeoutError:
			log('The server is busy (timeout error). Connect later', 'critical')
			self.client.close()
			exit()
		except ConnectionRefusedError:
			log('Check if you are connected to the network (if the server is not on local network) and if the server is turned on.', 'critical')
