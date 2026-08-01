
def test_compare_datetime_with_all_none():
    # GH#54870
    ser = Series(["2020-01-01", "2020-01-02"], dtype="datetime64[ns]")
    ser2 = Series([None, None])
    result = ser > ser2
    expected = Series([False, False])
    tm.assert_series_equal(result, expected)

