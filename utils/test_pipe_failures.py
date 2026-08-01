
def test_pipe_failures(any_string_dtype):
    # #2119
    ser = Series(["A|B|C"], dtype=any_string_dtype)

    result = ser.str.split("|")
    expected = Series([["A", "B", "C"]], dtype=object)
    tm.assert_series_equal(result, expected)

    result = ser.str.replace("|", " ", regex=False)
    expected = Series(["A B C"], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

