
def test_extract_single_group_returns_frame(any_string_dtype):
    # GH11386 extract should always return DataFrame, even when
    # there is only one group. Prior to v0.18.0, extract returned
    # Series when there was only one group in the regex.
    s = Series(["a3", "b3", "c2"], name="series_name", dtype=any_string_dtype)
    result = s.str.extract(r"(?P<letter>[a-z])", expand=True)
    expected = DataFrame({"letter": ["a", "b", "c"]}, dtype=any_string_dtype)
    tm.assert_frame_equal(result, expected)

