
def test_extractall_single_group(any_string_dtype):
    s = Series(["a3", "b3", "d4c2"], name="series_name", dtype=any_string_dtype)
    expected_index = MultiIndex.from_tuples(
        [(0, 0), (1, 0), (2, 0), (2, 1)], names=(None, "match")
    )

    # extractall(one named group) returns DataFrame with one named column.
    result = s.str.extractall(r"(?P<letter>[a-z])")
    expected = DataFrame(
        {"letter": ["a", "b", "d", "c"]}, index=expected_index, dtype=any_string_dtype
    )
    tm.assert_frame_equal(result, expected)

    # extractall(one un-named group) returns DataFrame with one un-named column.
    result = s.str.extractall(r"([a-z])")
    expected = DataFrame(
        ["a", "b", "d", "c"], index=expected_index, dtype=any_string_dtype
    )
    tm.assert_frame_equal(result, expected)

