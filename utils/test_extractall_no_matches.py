
def test_extractall_no_matches(data, names, any_string_dtype):
    # GH19075 extractall with no matches should return a valid MultiIndex
    n = len(data)
    if len(names) == 1:
        index = Index(range(n), name=names[0])
    else:
        tuples = (tuple([i] * (n - 1)) for i in range(n))
        index = MultiIndex.from_tuples(tuples, names=names)
    s = Series(data, name="series_name", index=index, dtype=any_string_dtype)
    expected_index = MultiIndex.from_tuples([], names=((*names, "match")))

    # one un-named group.
    result = s.str.extractall("(z)")
    expected = DataFrame(columns=range(1), index=expected_index, dtype=any_string_dtype)
    tm.assert_frame_equal(result, expected, check_column_type=True)

    # two un-named groups.
    result = s.str.extractall("(z)(z)")
    expected = DataFrame(columns=range(2), index=expected_index, dtype=any_string_dtype)
    tm.assert_frame_equal(result, expected, check_column_type=True)

    # one named group.
    result = s.str.extractall("(?P<first>z)")
    expected = DataFrame(
        columns=["first"], index=expected_index, dtype=any_string_dtype
    )
    tm.assert_frame_equal(result, expected)

    # two named groups.
    result = s.str.extractall("(?P<first>z)(?P<second>z)")
    expected = DataFrame(
        columns=["first", "second"], index=expected_index, dtype=any_string_dtype
    )
    tm.assert_frame_equal(result, expected)

    # one named, one un-named.
    result = s.str.extractall("(z)(?P<second>z)")
    expected = DataFrame(
        columns=[0, "second"], index=expected_index, dtype=any_string_dtype
    )
    tm.assert_frame_equal(result, expected)

