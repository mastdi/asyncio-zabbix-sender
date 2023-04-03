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
