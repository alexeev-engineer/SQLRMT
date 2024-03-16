#!/usr/bin/python3
"""SQLRMT
Software for working with remote SQL databases via the network.
SQLRMT is asynchronous, uses network traffic protection mechanisms and is extensible
SQLRMT - blazing fast tool for work with remote databases.

Copyright © 2024 Alexeev Bronislav. All rights reversed
"""
from datetime import datetime
from rich import print


def log(text: str, msg_type: str='info') -> str:
	"""Print beautiful debug message and save it to logfile.

	Arguments:
	---------
	 + text: str - message text (support rich formating)
	 + msg_type: str='info' - type of message (info, warn error, note, debug or unknown)

	Return:
	------
	+ str - message

	"""
	cleaned_text = text.replace("[bold]", '').replace("[/bold]", '')
	logfile_message = f'[{datetime.now()}] {msg_type} -- {cleaned_text}\n'

	if msg_type == 'info':
		msg = f'[green]INFO {datetime.now()}[/green] -- {text}'
	elif msg_type in ['warn', 'warning', 'caution']:
		msg = f'[yellow]CAUTION {datetime.now()}[/yellow] -- {text}'
	elif msg_type in ['error', 'err', 'ex', 'exception']:
		msg = f'[red]ERROR {datetime.now()}[/red] -- {text}'
	elif msg_type == 'note':
		msg = f'[blue]{datetime.now()}[/blue] -- {text}'
	elif msg_type == 'debug':
		msg = f'[cyan]DEBUG {datetime.now()}[/cyan] -- {text}'
	elif msg_type == 'none':
		msg = f'{text}'
	else:
		msg = f'[magenta]{msg_type.upper()} {datetime.now()}[/magenta] -- {text}'

	print(msg)

	with open('sqlrmt.log', 'a') as log:
		log.write(logfile_message)

	return msg
