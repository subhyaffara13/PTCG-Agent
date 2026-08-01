
def test_zfill(any_string_dtype):
    s = Series(["1", "22", "aaa", "333", "45678"], dtype=any_string_dtype)

    result = s.str.zfill(5)
    expected = Series(
        ["00001", "00022", "00aaa", "00333", "45678"], dtype=any_string_dtype
    )
    tm.assert_series_equal(result, expected)
    expected = np.array([v.zfill(5) for v in np.array(s)], dtype=np.object_)
    tm.assert_numpy_array_equal(np.array(result, dtype=np.object_), expected)

    result = s.str.zfill(3)
    expected = Series(["001", "022", "aaa", "333", "45678"], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)
    expected = np.array([v.zfill(3) for v in np.array(s)], dtype=np.object_)
    tm.assert_numpy_array_equal(np.array(result, dtype=np.object_), expected)

    s = Series(["1", np.nan, "aaa", np.nan, "45678"], dtype=any_string_dtype)
    result = s.str.zfill(5)
    expected = Series(
        ["00001", np.nan, "00aaa", np.nan, "45678"], dtype=any_string_dtype
    )
    tm.assert_series_equal(result, expected)


def test_zfill():
    # https://github.com/pandas-dev/pandas/issues/20868
    value = Series(["-1", "1", "1000", 10, np.nan])
    expected = Series(["-01", "001", "1000", np.nan, np.nan], dtype=object)
    tm.assert_series_equal(value.str.zfill(3), expected)

    value = Series(["-2", "+5"])
    expected = Series(["-0002", "+0005"])
    tm.assert_series_equal(value.str.zfill(5), expected)

