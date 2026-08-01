
def test_iso8601_formatter(date_str: str, timespec: str, exp: str):
    # GH#53020
    ts = Timestamp(date_str)
    assert ts.isoformat(timespec=timespec) == exp

