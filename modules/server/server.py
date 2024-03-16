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
from datetime import datetime
import threading
from rich import print


class Server:
	"""TLS-Server class

	Arguments:
	---------
	 + host: str - hostname
	 + port: int - port
	 + client_cert: str - client certification
	 + server_key: str - server secure key
	 + server_cert: str - server certification

	"""

	def __init__(self, host: str, port: int, client_cert: str, server_key: str, server_cert: str):
		self.host: str = host
		self.port: int = port
		self.client_cert: str = client_cert
		self.server_key: str = server_key
		self.server_cert: str = server_cert

		print(f'[blue]Create SSL context for {host}:{port}[/blue]')
		self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
		self.context.load_cert_chain(certfile=self.server_cert, keyfile=self.server_key)
		self.context.options |= ssl.OP_SINGLE_ECDH_USE
		self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2

		print(f'[blue]Create server socket ({host}:{port})[/blue]')
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.host, self.port))

	@cache
	def broadcast(self, conn, addr) -> None:
		while True:
			message = conn.recv(1024).decode()

			if message == 'DISCONNECT':
				print(f'{datetime.now()} -- {addr} disconnected')
				conn.close()
				return
			else:
				print(f'{datetime.now()} -- {addr} says: [bold]{message}[/bold]')
				conn.send(message.encode())

	@cache
	async def listen(self, max_conns: int=1) -> None:
		print('[blue]Listen connections...[/blue]')
	
		self.server.listen(2)
		
		with self.context.wrap_socket(self.server, server_side=True) as socks:
			while True:
				try:
					conn, addr = socks.accept()
					print(f'{datetime.now()} -- {addr} connected')

					thread = threading.Thread(target=lambda: self.broadcast(conn, addr))
					thread.daemon = True
					thread.start()
					thread.join()
				except ssl.SSLEOFError:
					print(f'[red]{datetime.now()} -- the second client tried to connect to the server[/red]')
