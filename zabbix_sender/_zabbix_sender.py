import asyncio
import typing

import zabbix_sender._measurements as _measurements
import zabbix_sender._protocol as _protocol
import zabbix_sender._response as _response


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

        return await self.send_packet(packet)

    async def send_packet(self, packet: bytes) -> _response.ZabbixResponse:
        """Send a packet to Zabbix including headers, compression and the like.

        :param packet: The packet ready to be sent.
        :return: The response from Zabbix.
        """
        reader, writer = await self._open_connection()

        # Write the packet to Zabbix
        writer.write(packet)
        await writer.drain()

        # Read the response
        response = await _protocol.read_response(reader)

        # Close the connection to Zabbix
        writer.close()
        await writer.wait_closed()

        # Parse the response
        payload = _protocol.parse_packet_parts(response)
        return _response.response_from_payload(payload)
