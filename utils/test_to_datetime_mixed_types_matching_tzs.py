
def test_to_datetime_mixed_types_matching_tzs():
    # GH#55793
    dtstr = "2023-11-01 09:22:03-07:00"
    ts = Timestamp(dtstr)
    arr = [ts, dtstr]
    res1 = to_datetime(arr)
    res2 = to_datetime(arr[::-1])[::-1]
    res3 = to_datetime(arr, format="mixed")
    res4 = DatetimeIndex(arr)

    expected = DatetimeIndex([ts, ts])
    tm.assert_index_equal(res1, expected)
    tm.assert_index_equal(res2, expected)
    tm.assert_index_equal(res3, expected)
    tm.assert_index_equal(res4, expected)

