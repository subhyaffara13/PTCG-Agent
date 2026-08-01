
def test_findall_end_of_string(any_string_dtype):
    # https://github.com/pandas-dev/pandas/pull/63613
    ser = Series(["baz", "bar", "bars", "bar\n"], dtype=any_string_dtype)

    # with dollar sign
    result = ser.str.findall("bar$")
    expected = Series([[], ["bar"], [], ["bar"]], dtype=object)
    tm.assert_series_equal(result, expected)

    # with \Z (ensure this is translated to \z for pyarrow)
    result = ser.str.findall(r"bar\Z")
    expected = Series([[], ["bar"], [], []], dtype=object)
    tm.assert_series_equal(result, expected)

    # ensure finding a literal \Z still works
    ser = Series([r"bar\Z", "bar", "bars", "bar\n"], dtype=any_string_dtype)
    result = ser.str.findall(r"bar\\Z")
    expected = Series([["bar\\Z"], [], [], []], dtype=object)
    tm.assert_series_equal(result, expected)

