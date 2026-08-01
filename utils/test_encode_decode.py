
def test_encode_decode(any_string_dtype):
    ser = Series(["a", "b", "a\xe4"], dtype=any_string_dtype).str.encode("utf-8")
    result = ser.str.decode("utf-8")
    expected = Series(["a", "b", "a\xe4"], dtype="str")
    tm.assert_series_equal(result, expected)

