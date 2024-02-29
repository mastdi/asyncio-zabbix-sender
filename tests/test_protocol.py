#  Copyright (c) 2024. Martin Storgaard Dieu <martin@storgaarddieu.com>
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
import struct
import zlib

import pytest

from asyncio_zabbix_sender import create_packet
from asyncio_zabbix_sender._protocol import (
    PacketParts,
    parse_packet_parts,
    read_response,
)
from tests.mock import MockStreamReader


def test_create_packet_without_compression():
    request = b'{"hello":"world"}'

    packet = create_packet(request, False)

    flags, data_length, reserved = struct.unpack("<BII", packet[4 : -len(request)])
    assert packet.startswith(b"ZBXD")
    assert flags == 0x01
    assert data_length == len(request)
    assert reserved == 0
    assert packet.endswith(request)


def test_create_packet_with_compression():
    request = b'{"hello":"world"}'
    expected_data = zlib.compress(request)

    packet = create_packet(request, True)

    flags, data_length, reserved = struct.unpack(
        "<BII", packet[4 : -len(expected_data)]
    )
    assert packet.startswith(b"ZBXD")
    assert flags == 0x01 | 0x02
    assert data_length == len(expected_data)
    assert reserved == len(request)
    assert packet.endswith(expected_data)


@pytest.mark.asyncio
async def test_read_response():
    request = b'{"hello":"world"}'
    packet = create_packet(request, False)
    reader = MockStreamReader(packet)

    response = await read_response(reader)

    assert response.data == request
    assert response.data_length == len(request)
    assert response.flags == 0x01
    assert response.protocol == b"ZBXD"
    assert response.reserved == 0


def test_parse_packet_parts():
    request = b'{"hello":"world"}'
    packet_parts = PacketParts(
        data=request, data_length=len(request), flags=0x01, protocol=b"ZBXD", reserved=0
    )

    parsed_request = parse_packet_parts(packet_parts)

    assert parsed_request == {"hello": "world"}


def test_parse_packet_parts_with_compression():
    request = b'{"hello":"world"}'
    compressed_request = zlib.compress(request)
    packet_parts = PacketParts(
        data=compressed_request,
        data_length=len(compressed_request),
        flags=0x01 | 0x02,
        protocol=b"ZBXD",
        reserved=len(request),
    )

    parsed_request = parse_packet_parts(packet_parts)

    assert parsed_request == {"hello": "world"}
