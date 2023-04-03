import datetime

from zabbix_sender._util import split_datetime


def test_split_datetime():
    now = datetime.datetime.utcnow()

    datetime_tuple = split_datetime(now)

    assert datetime_tuple.clock == int(now.timestamp())
    assert datetime_tuple.ns == now.microsecond * 1000
