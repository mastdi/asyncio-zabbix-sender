import asyncio


class MockStreamReader(asyncio.StreamReader):
    def __init__(self, stream: bytes) -> None:
        self._stream = stream
        self._index = 0

    async def readexactly(self, n: int) -> bytes:
        part = self._stream[self._index : self._index + n]
        self._index += n
        return part


class MockStreamWriter(asyncio.StreamWriter):
    def __init__(self):
        self.received_bytes = b""

    def write(self, data: bytes) -> None:
        self.received_bytes += data

    def close(self) -> None:
        pass

    async def wait_closed(self) -> None:
        pass

    async def drain(self) -> None:
        pass


def create_open_connection_mock(reader, writer):
    async def _open_connection():
        return reader, writer

    return _open_connection
