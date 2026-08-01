
def test_slice_mixed_object(start, stop, step, expected):
    ser = Series(["aafootwo", np.nan, "aabartwo", True, datetime.today(), None, 1, 2.0])
    result = ser.str.slice(start, stop, step)
    expected = Series(expected, dtype=object)
    tm.assert_series_equal(result, expected)

