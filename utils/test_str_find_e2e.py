
def test_str_find_e2e(start, end, sub):
    s = pd.Series(
        ["abcaadef", "abc", "abcdeddefgj8292", "ab", "a", ""],
        dtype=ArrowDtype(pa.string()),
    )
    object_series = s.astype(pd.StringDtype(storage="python"))
    result = s.str.find(sub, start, end)
    expected = object_series.str.find(sub, start, end).astype(result.dtype)
    tm.assert_series_equal(result, expected)

    arrow_str_series = s.astype(pd.StringDtype(storage="pyarrow"))
    result2 = arrow_str_series.str.find(sub, start, end).astype(result.dtype)
    tm.assert_series_equal(result2, expected)

