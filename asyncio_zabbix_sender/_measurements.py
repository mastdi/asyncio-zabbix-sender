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
import dataclasses
import datetime
import json
import typing

import asyncio_zabbix_sender._util as _util


@dataclasses.dataclass
class Measurement:
    """A single measurement corresponding to a single item or low-level discovery rule.

    Args:
        host: The hostname the item belongs to (as registered in Zabbix frontend).
        key: The item key to send the value to.
        value: The item value.
        clock: Timestamp should be specified in Unix timestamp format.
        ns: Additional nanoseconds precision of the Unix timestamp.

    """

    host: str
    key: str
    value: typing.Union[float, int, str]
    clock: typing.Optional[typing.Union[int, datetime.datetime]] = None
    ns: typing.Optional[int] = None

    def __post_init__(self):
        if isinstance(self.clock, datetime.datetime):
            split_datetime = _util.split_datetime(self.clock)
            if self.ns is None:
                self.ns = split_datetime.ns
            self.clock = split_datetime.clock

    def as_dict(self) -> typing.Dict[str, typing.Union[float, int, str]]:
        """Represent the measurement as a dict.

        :return: Optional values that are not set are left out of the representation.
        """
        measurement = {"host": self.host, "key": self.key, "value": self.value}
        if isinstance(self.clock, int):
            measurement["clock"] = self.clock
        if isinstance(self.ns, int):
            measurement["ns"] = self.ns

        return measurement


class Measurements:
    def __init__(
        self,
        measurements: typing.Optional[typing.List[Measurement]] = None,
        clock: typing.Optional[typing.Union[int, datetime.datetime]] = None,
        ns: typing.Optional[int] = None,
    ):
        """Create a collection of measurements ready for the ZabbixSender.

        :param clock: Optional time for this collection.
        :param ns: Optional nanoseconds for this collection.
        """
        if measurements is None:
            self._measurements: typing.List[Measurement] = []
        else:
            self._measurements = measurements
        self.clock = clock
        self.ns = ns
        if isinstance(self.clock, datetime.datetime):
            split_datetime = _util.split_datetime(self.clock)
            if self.ns is None:
                self.ns = split_datetime.ns
            self.clock = split_datetime.clock

    def add_measurement(self, measurement: Measurement):
        """Add a measurement to the collection of measurements.

        :param measurement: The measurement to be added.
        """
        self._measurements.append(measurement)

    def as_dict(self) -> typing.Dict[str, typing.Any]:
        """Represent the measurement as a Zabbix request.

        :return: Zabbix request as a dictionary.
        """
        measurements: typing.Dict[str, typing.Any] = {
            "request": "sender data",
            "data": [measurement.as_dict() for measurement in self._measurements],
        }
        if isinstance(self.clock, int):
            measurements["clock"] = self.clock
        if isinstance(self.ns, int):
            measurements["ns"] = self.ns
        return measurements

    def __str__(self) -> str:
        """Represent the measurement as a Zabbix request.

        :return: Zabbix request as a string.
        """
        return json.dumps(self.as_dict(), separators=(",", ":"), sort_keys=True)

    def __bytes__(self) -> bytes:
        """Represent the measurements as a Zabbix request.

        :return: Zabbix request as bytes.
        """
        return str(self).encode("utf-8")

    def __repr__(self) -> str:
        """Represent the measurements as the object in the current state.

        :return: Representation of the current state
        """
        parts = [type(self).__name__, "("]
        if len(self._measurements) > 0:
            parts.append("measurements=[")
            parts.append(
                ", ".join([repr(measurement) for measurement in self._measurements])
            )
            parts.append("], ")
        if self.clock is not None:
            parts.append(f"clock={self.clock}")
            parts.append(", ")
        if self.ns is not None:
            parts.append(f"ns={self.ns}")
        if parts[-1] == ", ":
            parts.pop()
        parts.append(")")
        return "".join(parts)

    def __len__(self) -> int:
        """Return the number of measurements currently in the collection.

        :return: Number of measurements
        """
        return len(self._measurements)

    def __iter__(self) -> typing.Generator[Measurement, None, None]:
        """Iterate all measurements

        :return: Generator with all measurements
        """
        for measurement in self._measurements:
            yield measurement
