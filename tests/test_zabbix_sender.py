#  Copyright (c) 2023. Martin Storgaard Dieu <martin@storgaarddieu.com>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import decimal
import json
import zlib

import pytest

from asyncio_zabbix_sender import Measurements, ZabbixSender, create_packet
from tests.mock import MockStreamReader, MockStreamWriter, create_open_connection_mock


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
    sender = ZabbixSender("mock-host", use_compression=True)
    sender._open_connection = create_open_connection_mock(reader, writer)

    measurements = Measurements()

    response = await sender.send(measurements)

    assert response.processed == 41
    assert response.failed == 2
    assert response.total == 43
    assert response.time == decimal.Decimal("31.41592")
    assert writer.received_bytes.endswith(zlib.compress(bytes(measurements)))
