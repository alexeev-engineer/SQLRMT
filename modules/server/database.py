#!/usr/bin/python3
"""SQLRMT
Software for working with remote SQL databases via the network.
SQLRMT is asynchronous, uses network traffic protection mechanisms and is extensible
SQLRMT - blazing fast tool for work with remote databases.

Copyright © 2024 Alexeev Bronislav. All rights reversed
"""
import sqlite3
from functools import cache

from modules.logger import log


def validate(query: str) -> bool:
	"""Function for checking SQL query for correctness
	This function creates a temporary database in memory, then executes an SQL command; 
	if an exception occurs, we ask the user if he really wants to use this function. If 
	the user responds that he wants to use this request, or there was no exception, then 
	we return True. If the user does not agree, then we return False.

	Arguments:
	---------
	 + query: str - SQL query

	Return:
	------
	 + bool (True/False)

	"""
	temp_db = sqlite3.connect(":memory:")

	try:
		temp_db.execute(query)
	except sqlite3.OperationalError as e:
		if str(e).split(':')[0] == 'no such table':
			return True

		print(f'Query "{query}" failed validation ({e}).\nDo you really want to do it? This may damage your database!')
		use_query = input('yes/no (default no) > ').lower()

		if use_query.startswith('y'):
			log(f'An unvalidated "{query}" request will be sent', 'warn')
			return True
		else:
			return False
	finally:
		temp_db.close()
	
	return True


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

	@cache
	def change_db(self, new_database_path: str):
		"""Change database.

		Arguments:
		---------
		+ new_database_path: str - new path to database file

		"""
		self.database_path = new_database_path
		self.connection = sqlite3.connect(self.new_database_path)
		self.cursor = self.connection.cursor()

	@cache
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
			output = f'An error occurred while executing the request: {ex}. Request failed'

		return output

	def close(self):
		"""Close DB connection."""
		self.connection.close()
