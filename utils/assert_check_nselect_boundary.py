
def assert_check_nselect_boundary(vals, dtype, method):
    # helper function for 'test_boundary_{dtype}' tests
    ser = Series(vals, dtype=dtype)
    result = getattr(ser, method)(3)
    expected_idxr = range(3) if method == "nsmallest" else range(3, 0, -1)
    expected = ser.loc[expected_idxr]
    tm.assert_series_equal(result, expected)

