
def test_extract_expand_single_capture_group(index_or_series, any_string_dtype):
    # single group renames series/index properly
    s_or_idx = index_or_series(["A1", "A2"], dtype=any_string_dtype)
    result = s_or_idx.str.extract(r"(?P<uno>A)\d", expand=False)

    expected = index_or_series(["A", "A"], name="uno", dtype=any_string_dtype)
    if index_or_series == Series:
        tm.assert_series_equal(result, expected)
    else:
        tm.assert_index_equal(result, expected)

