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


## Road map
The following improvements are planned (not necessary in order):

- Logging
- Encryption between the sender and Zabbix
- More documentation
