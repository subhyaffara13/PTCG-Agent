
def test_series_from_temporary_datetimeindex_readonly_data():
    # GH 63388
    arr = np.array(["2020-01-01", "2020-01-02"], dtype="datetime64[ns]")
    arr.flags.writeable = False
    ser = Series(DatetimeIndex(arr))
    assert not np.shares_memory(arr, get_array(ser))
    ser.iloc[0] = Timestamp("2020-01-01")
    expected = Series(
        [Timestamp("2020-01-01"), Timestamp("2020-01-02")], dtype="datetime64[ns]"
    )
    tm.assert_series_equal(ser, expected)

