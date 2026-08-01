
def test_decode_string_dtype(string_dtype):
    # https://github.com/pandas-dev/pandas/pull/60940
    ser = Series([b"a", b"b"])
    result = ser.str.decode("utf-8", dtype=string_dtype)
    expected = Series(["a", "b"], dtype=string_dtype)
    tm.assert_series_equal(result, expected)

