import datetime
import typing


class SplitDatetime(typing.NamedTuple):
    clock: int
    ns: int


def split_datetime(raw_datetime: datetime.datetime) -> SplitDatetime:
    return SplitDatetime(int(raw_datetime.timestamp()), raw_datetime.microsecond * 1000)
