
def test_extract_expand_capture_groups(any_string_dtype):
    s = Series(["A1", "B2", "C3"], dtype=any_string_dtype)
    # one group, no matches
    result = s.str.extract("(_)", expand=False)
    expected = Series([np.nan, np.nan, np.nan], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

    # two groups, no matches
    result = s.str.extract("(_)(_)", expand=False)
    expected = DataFrame(
        [[np.nan, np.nan], [np.nan, np.nan], [np.nan, np.nan]], dtype=any_string_dtype
    )
    tm.assert_frame_equal(result, expected)

    # one group, some matches
    result = s.str.extract("([AB])[123]", expand=False)
    expected = Series(["A", "B", np.nan], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

    # two groups, some matches
    result = s.str.extract("([AB])([123])", expand=False)
    expected = DataFrame(
        [["A", "1"], ["B", "2"], [np.nan, np.nan]], dtype=any_string_dtype
    )
    tm.assert_frame_equal(result, expected)

    # one named group
    result = s.str.extract("(?P<letter>[AB])", expand=False)
    expected = Series(["A", "B", np.nan], name="letter", dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

    # two named groups
    result = s.str.extract("(?P<letter>[AB])(?P<number>[123])", expand=False)
    expected = DataFrame(
        [["A", "1"], ["B", "2"], [np.nan, np.nan]],
        columns=["letter", "number"],
        dtype=any_string_dtype,
    )
    tm.assert_frame_equal(result, expected)

    # mix named and unnamed groups
    result = s.str.extract("([AB])(?P<number>[123])", expand=False)
    expected = DataFrame(
        [["A", "1"], ["B", "2"], [np.nan, np.nan]],
        columns=[0, "number"],
        dtype=any_string_dtype,
    )
    tm.assert_frame_equal(result, expected)

    # one normal group, one non-capturing group
    result = s.str.extract("([AB])(?:[123])", expand=False)
    expected = Series(["A", "B", np.nan], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

    # two normal groups, one non-capturing group
    s = Series(["A11", "B22", "C33"], dtype=any_string_dtype)
    result = s.str.extract("([AB])([123])(?:[123])", expand=False)
    expected = DataFrame(
        [["A", "1"], ["B", "2"], [np.nan, np.nan]], dtype=any_string_dtype
    )
    tm.assert_frame_equal(result, expected)

    # one optional group followed by one normal group
    s = Series(["A1", "B2", "3"], dtype=any_string_dtype)
    result = s.str.extract("(?P<letter>[AB])?(?P<number>[123])", expand=False)
    expected = DataFrame(
        [["A", "1"], ["B", "2"], [np.nan, "3"]],
        columns=["letter", "number"],
        dtype=any_string_dtype,
    )
    tm.assert_frame_equal(result, expected)

    # one normal group followed by one optional group
    s = Series(["A1", "B2", "C"], dtype=any_string_dtype)
    result = s.str.extract("(?P<letter>[ABC])(?P<number>[123])?", expand=False)
    expected = DataFrame(
        [["A", "1"], ["B", "2"], ["C", np.nan]],
        columns=["letter", "number"],
        dtype=any_string_dtype,
    )
    tm.assert_frame_equal(result, expected)

