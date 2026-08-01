
def test_decode_object_dtype(object_dtype):
    # https://github.com/pandas-dev/pandas/pull/60940
    ser = Series([b"a", rb"\ud800"])
    result = ser.str.decode("utf-8", dtype=object_dtype)
    expected = Series(["a", r"\ud800"], dtype=object_dtype)
    tm.assert_series_equal(result, expected)

