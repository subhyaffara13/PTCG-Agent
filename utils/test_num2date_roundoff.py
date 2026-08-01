
def test_num2date_roundoff():
    assert mdates.num2date(100000.0000578702) == datetime.datetime(
        2243, 10, 17, 0, 0, 4, 999980, tzinfo=datetime.timezone.utc)
    # Slightly larger, steps of 20 microseconds
    assert mdates.num2date(100000.0000578703) == datetime.datetime(
        2243, 10, 17, 0, 0, 5, tzinfo=datetime.timezone.utc)

