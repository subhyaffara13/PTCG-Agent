
def test_tz_utc():
    dt = datetime.datetime(1970, 1, 1, tzinfo=mdates.UTC)
    assert dt.tzname() == 'UTC'

