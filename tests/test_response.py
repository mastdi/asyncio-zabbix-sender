import decimal

from zabbix_sender._response import response_from_payload


def test_response_from_payload():
    payload = {
        "response": "success",
        "info": "processed: 41; failed: 2; total: 43; seconds spent: 31.41592",
    }

    response = response_from_payload(payload)

    assert response.processed == 41
    assert response.failed == 2
    assert response.total == 43
    assert response.time == decimal.Decimal("31.41592")
