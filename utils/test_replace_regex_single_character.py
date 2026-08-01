
def test_replace_regex_single_character(regex, any_string_dtype):
    # https://github.com/pandas-dev/pandas/pull/24809, enforced in 2.0
    # GH 24804
    s = Series(["a.b", ".", "b", np.nan, ""], dtype=any_string_dtype)

    result = s.str.replace(".", "a", regex=regex)
    if regex:
        expected = Series(["aaa", "a", "a", np.nan, ""], dtype=any_string_dtype)
    else:
        expected = Series(["aab", "a", "b", np.nan, ""], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

