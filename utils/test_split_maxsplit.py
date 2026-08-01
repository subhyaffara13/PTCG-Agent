
def test_split_maxsplit(data, pat, any_string_dtype, n):
    # re.split 0, str.split -1
    s = Series(data, dtype=any_string_dtype)

    result = s.str.split(pat=pat, n=n)
    xp = s.str.split(pat=pat)
    tm.assert_series_equal(result, xp)

