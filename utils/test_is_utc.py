
def test_is_utc(utc_fixture):
    tz = timezones.maybe_get_tz(utc_fixture)
    assert timezones.is_utc(tz)

