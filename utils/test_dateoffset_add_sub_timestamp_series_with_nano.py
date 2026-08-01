
def test_dateoffset_add_sub_timestamp_series_with_nano(offset, expected):
    # GH 47856
    start_time = Timestamp("2022-01-01")
    teststamp = start_time
    testseries = Series([start_time])
    testseries = testseries + offset
    assert testseries[0] == expected
    testseries -= offset
    assert testseries[0] == teststamp
    testseries = offset + testseries
    assert testseries[0] == expected

