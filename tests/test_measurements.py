import datetime

from zabbix_sender import Measurement, Measurements


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


def test_measurements_as_bytes():
    measurements = Measurements()

    representation = bytes(measurements)

    assert b'{"data":[],"request":"sender data"}' == representation
