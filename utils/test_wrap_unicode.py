
def test_wrap_unicode(any_string_dtype):
    # test with pre and post whitespace (non-unicode), NaN, and non-ascii Unicode
    s = Series(
        ["  pre  ", np.nan, "\xac\u20ac\U00008000 abadcafe"], dtype=any_string_dtype
    )
    expected = Series(
        ["  pre", np.nan, "\xac\u20ac\U00008000 ab\nadcafe"], dtype=any_string_dtype
    )
    result = s.str.wrap(6)
    tm.assert_series_equal(result, expected)

