
def test_extractall_single_group_with_quantifier(any_string_dtype):
    # GH#13382
    # extractall(one un-named group with quantifier) returns DataFrame with one un-named
    # column.
    s = Series(["ab3", "abc3", "d4cd2"], name="series_name", dtype=any_string_dtype)
    result = s.str.extractall(r"([a-z]+)")
    expected = DataFrame(
        ["ab", "abc", "d", "cd"],
        index=MultiIndex.from_tuples(
            [(0, 0), (1, 0), (2, 0), (2, 1)], names=(None, "match")
        ),
        dtype=any_string_dtype,
    )
    tm.assert_frame_equal(result, expected)

