
def test_to_datetime_mixed_other():
    # https://github.com/pandas-dev/pandas/issues/50411
    result = to_datetime(["01/11/2000", "12 January 2000"], format="mixed")
    expected = DatetimeIndex(["2000-01-11", "2000-01-12"])
    tm.assert_index_equal(result, expected)

