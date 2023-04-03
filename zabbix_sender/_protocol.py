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
import asyncio
import json
import struct
import typing
import zlib


class PacketParts(typing.NamedTuple):
    protocol: bytes
    flags: int
    data_length: int
    reserved: int
    data: bytes


def create_packet(request: bytes, use_compression: bool) -> bytes:
    """Create a Zabbix packet from a request.

    :param request: The encoded JSON body
    :param use_compression: If True, the request is compressed
    :return: The full packet ready to be sent to Zabbix
    """
    protocol = b"ZBXD"
    flags = 0x01
    data = request
    reserved = 0
    if use_compression:
        flags |= 0x02
        data = zlib.compress(request)
        reserved = len(request)

    return protocol + struct.pack("<BII", flags, len(data), reserved) + data


async def read_response(reader: asyncio.StreamReader) -> PacketParts:
    """Read response from the open stream.

    :param reader: The stream reader connected to a Zabbix Server/Proxy.
    :return: The packet.
    """
    header = await reader.readexactly(13)
    assert header.startswith(b"ZBXD"), header
    flags, data_length, reserved = struct.unpack("<BII", header[4:])

    data = await reader.readexactly(data_length)
    return PacketParts(b"ZBXD", flags, data_length, reserved, data)


def parse_packet_parts(packet_parts: PacketParts) -> typing.Dict[str, str]:
    """Parse the packet parts and the JSON payload to a dict.

    :param packet_parts: The packet parts
    :return: The parsed JSON payload
    """
    data = packet_parts.data
    if packet_parts.flags & 0x02 > 0:
        data = zlib.decompress(packet_parts.data)
        assert len(data) == packet_parts.reserved

    return json.loads(data)
