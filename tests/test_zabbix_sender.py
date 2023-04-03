import decimal
import json

import pytest

from tests.mock import MockStreamReader, MockStreamWriter, create_open_connection_mock
from zabbix_sender import Measurements, ZabbixSender, create_packet


@pytest.mark.asyncio
async def test_send():
    response = create_packet(
        json.dumps(
            {
                "response": "success",
                "info": "processed: 41; failed: 2; total: 43; seconds spent: 31.41592",
            }
        ).encode("utf8"),
        True,
    )
    reader = MockStreamReader(response)
    writer = MockStreamWriter()
    sender = ZabbixSender("mock-host", use_compression=False)
    sender._open_connection = create_open_connection_mock(reader, writer)

    measurements = Measurements()

    response = await sender.send(measurements)

    assert response.processed == 41
    assert response.failed == 2
    assert response.total == 43
    assert response.time == decimal.Decimal("31.41592")
    assert writer.received_bytes.endswith(bytes(measurements))
