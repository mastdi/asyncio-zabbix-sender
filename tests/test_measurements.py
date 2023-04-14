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
import datetime

from asyncio_zabbix_sender import Measurement, Measurements


def test_measurement_with_datetime():
    host = "zabbix-sender-host"
    key = "trapper.measurement"
    value = "unit test"
    now = datetime.datetime.utcnow()

    measurement = Measurement(host=host, key=key, value=value, clock=now)

    assert measurement.as_dict() == {
        "host": host,
        "key": key,
        "value": value,
        "clock": int(now.timestamp()),
        "ns": now.microsecond * 1000,
    }


def test_measurement_without_time():
    host = "zabbix-sender-host"
    key = "trapper.measurement"
    value = "unit test"

    measurement = Measurement(
        host=host,
        key=key,
        value=value,
    )

    assert measurement.as_dict() == {
        "host": host,
        "key": key,
        "value": value,
    }


def test_measurements_with_clock():
    clock = int(datetime.datetime.utcnow().timestamp())
    measurement = Measurement(
        host="zabbix-sender-host",
        key="trapper.measurement",
        value="unit test",
    )
    measurements = Measurements(clock=clock)
    measurements.add_measurement(measurement)

    representation = measurements.as_dict()

    assert representation["request"] == "sender data"
    assert len(representation["data"]) == 1
    assert representation["data"][0] == measurement.as_dict()
    assert representation["clock"] == clock
    assert "ns" not in representation


def test_measurements_from_constructor():
    measurement = Measurement(
        host="zabbix-sender-host",
        key="trapper.measurement",
        value="unit test",
    )
    measurements = Measurements([measurement])

    representation = measurements.as_dict()

    assert representation["request"] == "sender data"
    assert len(representation["data"]) == 1
    assert representation["data"][0] == measurement.as_dict()
    assert "clock" not in representation
    assert "ns" not in representation


def test_measurements_as_bytes():
    measurements = Measurements()

    representation = bytes(measurements)

    assert b'{"data":[],"request":"sender data"}' == representation


def test_measurements_repr():
    expected_measurements = Measurements(
        measurements=[Measurement("host", "key", "value", clock=601886899)],
        clock=574066099,
        ns=8123116,
    )

    representation = repr(expected_measurements)

    measurements = eval(representation)
    assert expected_measurements.clock == measurements.clock
    assert expected_measurements.ns == measurements.ns
    assert expected_measurements._measurements == expected_measurements._measurements


def test_measurements_repr_no_time():
    expected_measurements = Measurements(
        measurements=[
            Measurement("host", "key", "value", clock=601886899),
            Measurement("h", "k", "v"),
        ],
    )

    representation = repr(expected_measurements)

    measurements = eval(representation)
    assert expected_measurements.clock == measurements.clock
    assert expected_measurements.ns == measurements.ns
    assert expected_measurements._measurements == expected_measurements._measurements


def test_measurements_length():
    measurements = Measurements(
        measurements=[
            Measurement("host", "key", "value", clock=601886899),
            Measurement("h", "k", "v"),
        ],
    )

    assert len(measurements) == 2
