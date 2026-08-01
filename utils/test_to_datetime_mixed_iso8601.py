
def test_to_datetime_mixed_iso8601():
    # https://github.com/pandas-dev/pandas/issues/50411
    result = to_datetime(["2020-01-01", "2020-01-01 05:00:00"], format="ISO8601")
    expected = DatetimeIndex(["2020-01-01 00:00:00", "2020-01-01 05:00:00"])
    tm.assert_index_equal(result, expected)

