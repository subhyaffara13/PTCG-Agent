
def test_decode_with_dtype_none():
    with option_context("future.infer_string", True):
        ser = Series([b"a", b"b", b"c"])
        result = ser.str.decode("utf-8", dtype=None)
        expected = Series(["a", "b", "c"], dtype="str")
        tm.assert_series_equal(result, expected)

