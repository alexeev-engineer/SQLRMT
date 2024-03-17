#!/usr/bin/python3
"""SQLRMT
Software for working with remote SQL databases via the network.
SQLRMT is asynchronous, uses network traffic protection mechanisms and is extensible
SQLRMT - blazing fast tool for work with remote databases.

Copyright © 2024 Alexeev Bronislav. All rights reversed
"""
from pysqlcipher3 import dbapi2 as sqlite3


class DBManager:
	"""Database manager.

	This class interacts with the database and works with SQL queries
	
	Arguments:
	---------
	 + database_path: str - path to database file

	"""

	def __init__(self, database_path: str):
		self.database_path = database_path
		self.connection = sqlite3.connect(self.database_path)
		self.cursor = self.connection.cursor()
		self.queries_count = {
			'success': 0,
			'failed': 0
		}
		self.total_queries_count = 0

	def set_pass(self, passphrase) -> list:
		try:
			self.connection.execute(f"PRAGMA key = '{passphrase}'")
		except Exception as e:
			return [False, f'Password verification failed when connecting to the database ({e})']
		else:
			return [True, 'Verification passed. Successful connection to the database.']

	def change_db(self, new_database_path: str):
		"""Change database.

		Arguments:
		---------
		+ new_database_path: str - new path to database file

		"""
		self.database_path = new_database_path
		self.connection = sqlite3.connect(self.database_path)
		self.cursor = self.connection.cursor()

	def info_about_database(self) -> str:
		return f'Database: {self.database_path}. Total queries sended: {self.total_queries_count}; success - {self.queries_count["success"]}; failed - {self.queries_count["failed"]}'

	def execute(self, query: str) -> str:
		"""Execute SQL Query.

		Arguments:
		---------
		+ query: str - sql query

		"""
		output = ''
		self.total_queries_count += 1

		try:
			self.cursor.execute(query)
			data = self.cursor.fetchall()

			if data:
				output = str(data)
			else:
				output = f'Request "{query}" completed successfully'

			self.connection.commit()
		except Exception as ex:
			output = f'An error occurred while executing the request: {ex}'
			self.queries_count['failed'] += 1
		else:
			self.queries_count['success'] += 1

		return output

	def close(self):
		"""Close DB connection."""
		self.connection.close()
