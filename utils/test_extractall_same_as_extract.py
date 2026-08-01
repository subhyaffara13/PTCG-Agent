
def test_extractall_same_as_extract(any_string_dtype):
    s = Series(["a3", "b3", "c2"], name="series_name", dtype=any_string_dtype)

    pattern_two_noname = r"([a-z])([0-9])"
    extract_two_noname = s.str.extract(pattern_two_noname, expand=True)
    has_multi_index = s.str.extractall(pattern_two_noname)
    no_multi_index = has_multi_index.xs(0, level="match")
    tm.assert_frame_equal(extract_two_noname, no_multi_index)

    pattern_two_named = r"(?P<letter>[a-z])(?P<digit>[0-9])"
    extract_two_named = s.str.extract(pattern_two_named, expand=True)
    has_multi_index = s.str.extractall(pattern_two_named)
    no_multi_index = has_multi_index.xs(0, level="match")
    tm.assert_frame_equal(extract_two_named, no_multi_index)

    pattern_one_named = r"(?P<group_name>[a-z])"
    extract_one_named = s.str.extract(pattern_one_named, expand=True)
    has_multi_index = s.str.extractall(pattern_one_named)
    no_multi_index = has_multi_index.xs(0, level="match")
    tm.assert_frame_equal(extract_one_named, no_multi_index)

    pattern_one_noname = r"([a-z])"
    extract_one_noname = s.str.extract(pattern_one_noname, expand=True)
    has_multi_index = s.str.extractall(pattern_one_noname)
    no_multi_index = has_multi_index.xs(0, level="match")
    tm.assert_frame_equal(extract_one_noname, no_multi_index)

