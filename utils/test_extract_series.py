
def test_extract_series(name, any_string_dtype):
    # extract should give the same result whether or not the series has a name.
    s = Series(["A1", "B2", "C3"], name=name, dtype=any_string_dtype)

    # one group, no matches
    result = s.str.extract("(_)", expand=True)
    expected = DataFrame([np.nan, np.nan, np.nan], dtype=any_string_dtype)
    tm.assert_frame_equal(result, expected)

    # two groups, no matches
    result = s.str.extract("(_)(_)", expand=True)
    expected = DataFrame(
        [[np.nan, np.nan], [np.nan, np.nan], [np.nan, np.nan]], dtype=any_string_dtype
    )
    tm.assert_frame_equal(result, expected)

    # one group, some matches
    result = s.str.extract("([AB])[123]", expand=True)
    expected = DataFrame(["A", "B", np.nan], dtype=any_string_dtype)
    tm.assert_frame_equal(result, expected)

    # two groups, some matches
    result = s.str.extract("([AB])([123])", expand=True)
    expected = DataFrame(
        [["A", "1"], ["B", "2"], [np.nan, np.nan]], dtype=any_string_dtype
    )
    tm.assert_frame_equal(result, expected)

    # one named group
    result = s.str.extract("(?P<letter>[AB])", expand=True)
    expected = DataFrame({"letter": ["A", "B", np.nan]}, dtype=any_string_dtype)
    tm.assert_frame_equal(result, expected)

    # two named groups
    result = s.str.extract("(?P<letter>[AB])(?P<number>[123])", expand=True)
    expected = DataFrame(
        [["A", "1"], ["B", "2"], [np.nan, np.nan]],
        columns=["letter", "number"],
        dtype=any_string_dtype,
    )
    tm.assert_frame_equal(result, expected)

    # mix named and unnamed groups
    result = s.str.extract("([AB])(?P<number>[123])", expand=True)
    expected = DataFrame(
        [["A", "1"], ["B", "2"], [np.nan, np.nan]],
        columns=[0, "number"],
        dtype=any_string_dtype,
    )
    tm.assert_frame_equal(result, expected)

    # one normal group, one non-capturing group
    result = s.str.extract("([AB])(?:[123])", expand=True)
    expected = DataFrame(["A", "B", np.nan], dtype=any_string_dtype)
    tm.assert_frame_equal(result, expected)

