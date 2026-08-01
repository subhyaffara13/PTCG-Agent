
def test_chrono_duration_roundtrip():
    # Get the difference between two times (a timedelta)
    date1 = datetime.datetime.today()
    date2 = datetime.datetime.today()
    diff = date2 - date1

    # Make sure this is a timedelta
    assert isinstance(diff, datetime.timedelta)

    cpp_diff = m.test_chrono3(diff)

    assert cpp_diff == diff

    # Negative timedelta roundtrip
    diff = datetime.timedelta(microseconds=-1)
    cpp_diff = m.test_chrono3(diff)

    assert cpp_diff == diff

