
def test_NanosecondGeneric():
    timestamp = Timestamp(datetime(2010, 1, 1))
    assert timestamp.nanosecond == 0

    result = timestamp + Nano(10)
    assert result.nanosecond == 10

    reverse_result = Nano(10) + timestamp
    assert reverse_result.nanosecond == 10

