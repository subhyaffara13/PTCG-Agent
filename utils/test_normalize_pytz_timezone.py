
def test_normalize_pytz_timezone():
    pytz = pytest.importorskip("pytz")

    from pandas.io._util import _normalize_pytz_timezone

    for tz, expected in [
        (pytz.UTC, timezone.utc),
        (pytz.FixedOffset(90), timezone(timedelta(minutes=90))),
        (pytz.timezone("America/New_York"), zoneinfo.ZoneInfo("America/New_York")),
        (pytz.timezone("Etc/GMT+1"), zoneinfo.ZoneInfo("Etc/GMT+1")),
    ]:
        result = _normalize_pytz_timezone(tz)
        assert result == expected

