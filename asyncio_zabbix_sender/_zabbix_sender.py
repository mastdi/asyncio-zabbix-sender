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
import logging
import typing

import asyncio_zabbix_sender._measurements as _measurements
import asyncio_zabbix_sender._protocol as _protocol
import asyncio_zabbix_sender._response as _response


class ZabbixSender:
    def __init__(
        self,
        zabbix_host: str,
        zabbix_port: typing.Union[int, str] = 10051,
        use_compression=True,
    ):
        """The Zabbix sender for sending either a measurement collection or a raw
        packet.

        :param zabbix_host: The hostname/IP of the Zabbix Server
        :param zabbix_port: The port of the Zabbix Server
        :param use_compression: If True, then measurement collection will be compressed
                                and otherwise the packet will be sent without
                                compression. This does not apply if send_packet is used.
        """
        self.zabbix_host = zabbix_host
        self.zabbix_port = zabbix_port
        self.use_compression = use_compression
        self.logger = logging.getLogger("asyncio-zabbix-sender")

    async def _open_connection(
        self,
    ) -> typing.Tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        """Open a connection to Zabbix

        :return: A stream reader and writer pair.
        """
        return await asyncio.open_connection(self.zabbix_host, self.zabbix_port)

    async def send(
        self, measurements: _measurements.Measurements
    ) -> _response.ZabbixResponse:
        """Send the measurements to Zabbix

        :param measurements: The measurement collection.
        :return: The response from Zabbix.
        """
        packet = _protocol.create_packet(bytes(measurements), self.use_compression)
        self.logger.debug(
            "Created packet from measurements. Used compression: %r.",
            self.use_compression,
        )
        return await self.send_packet(packet)

    async def send_packet(self, packet: bytes) -> _response.ZabbixResponse:
        """Send a packet to Zabbix including headers, compression and the like.

        :param packet: The packet ready to be sent.
        :return: The response from Zabbix.
        """
        reader, writer = await self._open_connection()

        # Write the packet to Zabbix
        self.logger.debug("Sending packet: %r", packet)
        writer.write(packet)
        await writer.drain()

        # Read the response
        response = await _protocol.read_response(reader)
        self.logger.debug("Got response: %r", response.data)

        # Close the connection to Zabbix
        self.logger.info(
            "Packet sent: %d bytes. Response data received: %d bytes. "
            "Response flags %d.",
            len(packet),
            response.data_length,
            response.flags,
        )
        writer.close()
        await writer.wait_closed()

        # Parse the response
        payload = _protocol.parse_packet_parts(response)
        self.logger.debug("Parsed response payload: %r", payload)
        return _response.response_from_payload(payload)
