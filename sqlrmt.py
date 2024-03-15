#!/usr/bin/python3
"""SQLRMT
Software for working with remote SQL databases via the network.
SQLRMT is asynchronous, uses network traffic protection mechanisms and is extensible
SQLRMT - blazing fast tool for work with remote databases.

Copyright © 2024 Alexeev Bronislav. All rights reversed
"""
from functools import cache
from time import monotonic
from rich import print
import asyncio

__version__ = '0.1.0'
__author__ = 'Alexeev Bronislav'


@cache
async def main():
	"""Main function."""
	print(f'SQLRMT {__version__} @ {__author__}')
	print('Run with `--help` flag to view help\n')
	
	start = monotonic()
	end = monotonic()
	total = round(end - start, 3)

	print(f'\nConnection uptime: {total} sec.')


if __name__ == '__main__':
	"""Run tasks"""
	asyncio.run(main())
