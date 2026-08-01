
def test_center_ljust_rjust_fillchar(any_string_dtype):
    # GH#54533, GH#54792
    s = Series(["a", "bb", "cccc", "ddddd", "eeeeee"], dtype=any_string_dtype)

    result = s.str.center(5, fillchar="X")
    expected = Series(
        ["XXaXX", "XXbbX", "Xcccc", "ddddd", "eeeeee"], dtype=any_string_dtype
    )
    tm.assert_series_equal(result, expected)
    expected = np.array([v.center(5, "X") for v in np.array(s)], dtype=np.object_)
    tm.assert_numpy_array_equal(np.array(result, dtype=np.object_), expected)

    result = s.str.ljust(5, fillchar="X")
    expected = Series(
        ["aXXXX", "bbXXX", "ccccX", "ddddd", "eeeeee"], dtype=any_string_dtype
    )
    tm.assert_series_equal(result, expected)
    expected = np.array([v.ljust(5, "X") for v in np.array(s)], dtype=np.object_)
    tm.assert_numpy_array_equal(np.array(result, dtype=np.object_), expected)

    result = s.str.rjust(5, fillchar="X")
    expected = Series(
        ["XXXXa", "XXXbb", "Xcccc", "ddddd", "eeeeee"], dtype=any_string_dtype
    )
    tm.assert_series_equal(result, expected)
    expected = np.array([v.rjust(5, "X") for v in np.array(s)], dtype=np.object_)
    tm.assert_numpy_array_equal(np.array(result, dtype=np.object_), expected)

