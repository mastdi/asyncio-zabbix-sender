# Zabbix sender
Dependency free implementation of the Zabbix Sender protocol using asyncio.

Key features:
- **Full specification** implemented compared to other Zabbix sender implementations
- **Compression** is enabled as default
- **Asynchronous** implementation allows the program to continue while waiting for a response from Zabbix

## Installation
The package can be found on PyPI and installed using pip:
```commandline
pip install zabbix-sender
```

## Usage

```python
import datetime
from zabbix_sender import ZabbixSender, Measurements, Measurement

sender = ZabbixSender("example.com")

measurements = Measurements()
measurements.add_measurement(Measurement(
    "vm-game-server", "cheat[doom]", "idkfa", datetime.datetime.utcnow()
))

await sender.send(measurements)
```


## Road map
The following improvements are planned (not necessary in order):

- Logging
- Encryption between the sender and Zabbix
- More documentation
