<p align="center">
	<img src="docs/sqlrmt.png">
</p>

<p align="center">Software for working with remote SQL databases via the network.</p>
<br>
<p align="center">
    <img src="https://img.shields.io/github/languages/top/alexeev-engineer/SQLRMT?style=for-the-badge">
    <img src="https://img.shields.io/github/languages/count/alexeev-engineer/SQLRMT?style=for-the-badge">
    <img src="https://img.shields.io/github/stars/alexeev-engineer/SQLRMT?style=for-the-badge">
    <img src="https://img.shields.io/github/issues/alexeev-engineer/SQLRMT?style=for-the-badge">
    <img src="https://img.shields.io/github/last-commit/alexeev-engineer/SQLRMT?style=for-the-badge">
    </br>
</p>

> **SQLRMT** is blazing fast software for connecting and managing your SQL databases in Python!

SQLRMT is asynchronous, uses network traffic protection mechanisms and is extensible.

> [!CAUTION]
> **SQLRMT currently only supports Linux distributions.** Other operating systems such as Windows, MacOS, BSD are not supported.

> [!CAUTION]
> At the moment, SQLRMT is under active development, many things may not work, and this version is not recommended for use (all at your own risk).

## Requirements

> [!NOTE]
> SQLRMT offers the use of a client-server model without the ability to connect multiple clients to one server address.

To run the software you will have to install the necessary programs and dependencies, such as:

 + Python interpreter (>=3.10)
 + PIP package manager (>=22.0)
 + Python libraries (listed in [requirements.txt](./requirements.txt))

## Installing
If you want to download a stable release, go to the [releases page](https://github.com/alexeev-engineer/SQLRMT/releases). If you want to install the latest git version, then follow these steps:

1. Clone this repo

```bash
git clone https://github.com/alexeev-engineer/SQLRMT.git
cd SQLRMT
```

2. Create a working virtual environment and install dependencies

> [!NOTE]
> If your shell is fish, then instead of `source venv/bin/activate` use `source venv/bin/activate.fish`.

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

3. Done! 💪 🎉  You're ready to use SQLRMT!

## Configuration
Before starting, you need to create or modify a configuration file `sqlrmt.ini`. The configuration file must be stored either in the program's working directory or in the path `/etc/sqlrmt.ini`

```ini
[Server]
host=127.0.0.1
port=8000

[Client]
database=database.sqlite
timeout=3
```

 + **Server** - server information
  - *host* - IP address (hostname)
  - *port* - port
 + **Client** - client information
  - *database* - path to connected database in server
  - *timeout* - timeout for connecting to server

## Functional
Here you can see what SQLRMT can already do and what else is planned to be added in the future:

 - [x] Asynchrony support
 - [x] Secure and protected connection
 - [ ] Extensions support
 - [ ] SQL Query Validation

## Copyright
SQLRMT - blazing fast tool for work with remote databases.

Copyright © 2024 Alexeev Bronislav. All rights reversed.

The registered trademark Linux® is used pursuant to a sublicense from LMI, the exclusive licensee of Linus Torvalds, owner of the mark on a world-wide basis.
