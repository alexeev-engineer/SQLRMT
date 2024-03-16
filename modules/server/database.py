#!/usr/bin/python3
"""SQLRMT
Software for working with remote SQL databases via the network.
SQLRMT is asynchronous, uses network traffic protection mechanisms and is extensible
SQLRMT - blazing fast tool for work with remote databases.

Copyright © 2024 Alexeev Bronislav. All rights reversed
"""
import sqlite3


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

	def change_db(self, new_database_path: str):
		"""Change database.

		Arguments:
		---------
		+ new_database_path: str - new path to database file

		"""
		self.database_path = new_database_path
		self.connection = sqlite3.connect(self.new_database_path)
		self.cursor = self.connection.cursor()

	def execute(self, query: str) -> str:
		"""Execute SQL Query.

		Arguments:
		---------
		+ query: str - sql query

		"""
		output = ''

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

		return output

	def close(self):
		"""Close DB connection."""
		self.connection.close()
