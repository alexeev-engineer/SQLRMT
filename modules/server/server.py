#!/usr/bin/python3
"""SQLRMT
Software for working with remote SQL databases via the network.
SQLRMT is asynchronous, uses network traffic protection mechanisms and is extensible
SQLRMT - blazing fast tool for work with remote databases.

Copyright © 2024 Alexeev Bronislav. All rights reversed
"""
import socket
import ssl
from functools import cache
import threading

from modules.logger import log
from modules.server.database import DBManager


class Server:
	"""TLS-Server class.

	Arguments:
	---------
	 + host: str - hostname
	 + port: int - port
	 + client_cert: str - client certification
	 + server_key: str - server secure key
	 + server_cert: str - server certification

	"""

	def __init__(self, host: str, port: int, client_cert: str, server_key: str, server_cert: str, server_db: str):
		self.host: str = host
		self.port: int = port
		self.client_cert: str = client_cert
		self.server_key: str = server_key
		self.server_cert: str = server_cert
		self.server_db: str = server_db

		# Create SSL context
		log(f'Create SSL context for {host}:{port}', 'debug')
		self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
		self.context.load_cert_chain(certfile=self.server_cert, keyfile=self.server_key)
		self.context.options |= ssl.OP_SINGLE_ECDH_USE
		self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2

		# Create socket
		log(f'Create server socket ({host}:{port})', 'debug')
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.host, self.port))

	@cache
	def broadcast(self, conn, addr: tuple) -> None:
		"""Broadcast messages and manage connection.

		Arguments:
		---------
		 + conn - connected socket (client)
		 + addr - client address

		"""
		dbman = DBManager(self.server_db)		# Database manager

		while True:
			# Receive and send message
			try:
				message = conn.recv(1024).decode()
			except ssl.SSLError as ex:
				log(f'The response was not received due to an error on the server: {ex}', 'error')
				conn.send(f'The response was not received due to an error on the server: {ex}'.encode())
				continue

			if message == 'DISCONNECT':
				# If client want to disconnect
				log(f'{addr} disconnected', 'warn')
				dbman.close()
				conn.close()
				return
			else:
				log(f'{addr} says: [bold]{message}[/bold]', 'note')
	
				response = dbman.execute(message)
				conn.send(response.encode())

	@cache
	async def listen(self, max_conns: int=1) -> None:
		"""Listen connections and create broadcast threads.

		Arguments:
		---------
		+ max_conns: int=1 - max connections number for listening

		"""
		log('Listen connections...', 'debug')

		# Listen connections
		self.server.listen(max_conns)
		
		# Wrap socket and create thread for broadcast
		with self.context.wrap_socket(self.server, server_side=True) as socks:
			while True:
				try:
					conn, addr = socks.accept()
					log(f'{addr} connected', 'info')

					thread = threading.Thread(target=lambda: self.broadcast(conn, addr))
					thread.daemon = True
					thread.start()
					thread.join()
				except ssl.SSLEOFError:
					log('the second client tried to connect to the server', 'debug')
