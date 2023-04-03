import asyncio


class MockStreamReader(asyncio.StreamReader):
    def __init__(self, stream: bytes) -> None:
        self._stream = stream
        self._index = 0

    async def readexactly(self, n: int) -> bytes:
        part = self._stream[self._index : self._index + n]
        self._index += n
        return part
