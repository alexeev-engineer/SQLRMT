#!/usr/bin/python3
"""SQLRMT
Software for working with remote SQL databases via the network.
SQLRMT is asynchronous, uses network traffic protection mechanisms and is extensible
SQLRMT - blazing fast tool for work with remote databases.

Copyright © 2024 Alexeev Bronislav. All rights reversed
"""
from paintlog.logger import Logger

logger = Logger('sqlrmt.log')


def log(msg_text: str, msg_type: str='info'):
	match msg_type:
		case 'debug':
			logger.log(msg_text, 'debug')
		case 'info':
			logger.log(msg_text, 'info')
		case 'warn':
			logger.log(msg_text, 'warn')
		case 'error':
			logger.log(msg_text, 'error')
		case 'exception':
			logger.log(msg_text, 'exception')
		case 'critical':
			logger.log(msg_text, 'exception')
		case 'none':
			print(msg_text)
		case _:
			logger.log(msg_text, msg_type.upper())
