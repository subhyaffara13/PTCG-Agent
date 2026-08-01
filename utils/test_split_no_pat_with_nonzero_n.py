
def test_split_no_pat_with_nonzero_n(data, pat, expected_val, any_string_dtype):
    s = Series(data, dtype=any_string_dtype)
    result = s.str.split(pat=pat, n=1)
    expected = Series({0: ["split", "once"], 1: ["split", expected_val]})
    tm.assert_series_equal(expected, result, check_index_type=False)

