
def test_chrono_system_clock_roundtrip():
    date1 = datetime.datetime.today()

    # Roundtrip the time
    date2 = m.test_chrono2(date1)

    # The returned value should be a datetime
    assert isinstance(date2, datetime.datetime)

    # They should be identical (no information lost on roundtrip)
    diff = abs(date1 - date2)
    assert diff == datetime.timedelta(0)

