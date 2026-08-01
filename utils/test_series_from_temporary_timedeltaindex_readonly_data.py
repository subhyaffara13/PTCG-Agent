
def test_series_from_temporary_timedeltaindex_readonly_data():
    # GH 63388
    arr = np.array([1, 2], dtype="timedelta64[ns]")
    arr.flags.writeable = False
    ser = Series(TimedeltaIndex(arr))
    assert not np.shares_memory(arr, get_array(ser))
    ser.iloc[0] = Timedelta(days=1)
    expected = Series(
        [Timedelta(days=1), Timedelta(nanoseconds=2)], dtype="timedelta64[ns]"
    )
    tm.assert_series_equal(ser, expected)

