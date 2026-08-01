
def test_extractall_lookarounds(any_string_dtype, pat, expected_data):
    # https://github.com/pandas-dev/pandas/issues/60833
    ser = Series(["aa", "ab", "ba", "bb", None], dtype=any_string_dtype)
    result = ser.str.extractall(pat)
    expected = Series(expected_data, dtype=any_string_dtype).to_frame()
    expected.index.names = [None, "match"]
    tm.assert_frame_equal(result, expected)

