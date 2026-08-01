
def test_extractall_same_as_extract_subject_index(any_string_dtype):
    # same as above tests, but s has a MultiIndex.
    mi = MultiIndex.from_tuples(
        [("A", "first"), ("B", "second"), ("C", "third")],
        names=("capital", "ordinal"),
    )
    s = Series(["a3", "b3", "c2"], index=mi, name="series_name", dtype=any_string_dtype)

    pattern_two_noname = r"([a-z])([0-9])"
    extract_two_noname = s.str.extract(pattern_two_noname, expand=True)
    has_match_index = s.str.extractall(pattern_two_noname)
    no_match_index = has_match_index.xs(0, level="match")
    tm.assert_frame_equal(extract_two_noname, no_match_index)

    pattern_two_named = r"(?P<letter>[a-z])(?P<digit>[0-9])"
    extract_two_named = s.str.extract(pattern_two_named, expand=True)
    has_match_index = s.str.extractall(pattern_two_named)
    no_match_index = has_match_index.xs(0, level="match")
    tm.assert_frame_equal(extract_two_named, no_match_index)

    pattern_one_named = r"(?P<group_name>[a-z])"
    extract_one_named = s.str.extract(pattern_one_named, expand=True)
    has_match_index = s.str.extractall(pattern_one_named)
    no_match_index = has_match_index.xs(0, level="match")
    tm.assert_frame_equal(extract_one_named, no_match_index)

    pattern_one_noname = r"([a-z])"
    extract_one_noname = s.str.extract(pattern_one_noname, expand=True)
    has_match_index = s.str.extractall(pattern_one_noname)
    no_match_index = has_match_index.xs(0, level="match")
    tm.assert_frame_equal(extract_one_noname, no_match_index)

