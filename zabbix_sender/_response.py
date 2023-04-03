import decimal
import re
import typing

_INFO_REGEX = re.compile(
    r"[Pp]rocessed:? (\d*);? [Ff]ailed:? (\d*);? [Tt]otal:? (\d*);? "
    r"[Ss]econds spent:? (\d*\.\d*)"
)


class ZabbixResponse(typing.NamedTuple):
    processed: int
    failed: int
    total: int
    time: decimal.Decimal


def response_from_payload(payload: typing.Dict[str, str]) -> ZabbixResponse:
    assert payload.get("response") == "success", payload
    info = payload.get("info")
    assert info is not None

    info_match = _INFO_REGEX.match(info)
    assert info_match is not None

    info_groups = info_match.groups()
    return ZabbixResponse(
        int(info_groups[0]),
        int(info_groups[1]),
        int(info_groups[2]),
        decimal.Decimal(info_groups[3]),
    )
