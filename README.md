# Zabbix sender
Dependency free implementation of the Zabbix Sender protocol using asyncio.

Key features:
- **Full specification** implemented compared to other Zabbix sender implementations
- **Compression** is enabled as default
- **Asynchronous** implementation allows the program to continue while waiting for a response from Zabbix

## Installation
The package can be found on PyPI and installed using pip:
```commandline
pip install asyncio-zabbix-sender
```

## Usage

```python
import datetime
from asyncio_zabbix_sender import ZabbixSender, Measurements, Measurement

sender = ZabbixSender("example.com")

measurements = Measurements([
    Measurement(
        "vm-game-server", "cheat.used[doom,player1]", "idkfa", datetime.datetime.utcnow()
    )
])

response = await sender.send(measurements)
```

## Logging
The logger can be configured by using the name `asyncio-zabbix-sender`:

```python
import logging

logger = logging.getLogger("asyncio-zabbix-sender")
logger.setLevel(logging.DEBUG)
```

Example from the `test_send` unit test by running pytest with `--log-cli-level=DEBUG`:
```text

DEBUG    asyncio-zabbix-sender:_protocol.py:47 Compressed packet: 40 bytes. Original 35.
DEBUG    asyncio-zabbix-sender:_zabbix_sender.py:63 Created packet from measurements. Used compression: True.
DEBUG    asyncio-zabbix-sender:_zabbix_sender.py:78 Sending packet: b'ZBXD\x03(\x00\x00\x00#\x00\x00\x00x\x9c\xabVJI,IT\xb2\x8a\x8e\xd5Q*J-,M-.Q\xb2R*N\xcdKI-R\x00K\xd5\x02\x00\xd3\xc2\x0b\xfb'
DEBUG    asyncio-zabbix-sender:_zabbix_sender.py:84 Got response: b'x\x9c\x15\xc8\xc1\n\x80 \x0c\x00\xd0_\x19;G\xa0\xd9!\xfd\x1a\xd1\t\x82l\xe2\xec\x14\xfd{y{\xbc\x07\x07i\x17VB\x0f\xa8wJ\xa4\x8a\x1b`\xe5"\xab\xfa\x90U\x94=8\x13\xa0\xc4\xda\x96m\x80)3\xb6\x7f\x8f\x00JI8+h\'\x9e\x1e\x0e\xb3;s^\x16\xdf\x0f\xc8\xd6\x1d\xb5'
INFO     asyncio-zabbix-sender:_zabbix_sender.py:87 Packet sent: 53 bytes. Response data received: 88 bytes. Response flags 3.
DEBUG    asyncio-zabbix-sender:_zabbix_sender.py:97 Parsed response payload: {'response': 'success', 'info': 'processed: 41; failed: 2; total: 43; seconds spent: 31.41592'}
```

Note that only a summary of the packet that are send and the response received are logged as informational.
Everything else is logged at debug level.

## Road map
The following improvements are planned (not necessary in order):

- Encryption between the sender and Zabbix
- Better error handling
- More documentation
