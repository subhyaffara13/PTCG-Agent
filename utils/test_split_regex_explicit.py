import re

def test_split_regex_explicit(any_string_dtype):
    # explicit regex = True split with compiled regex
    regex_pat = re.compile(r".jpg")
    values = Series("xxxjpgzzz.jpg", dtype=any_string_dtype)
    result = values.str.split(regex_pat)
    exp = Series([["xx", "zzz", ""]])
    tm.assert_series_equal(result, exp)

    # explicit regex = False split
    result = values.str.split(r"\.jpg", regex=False)
    exp = Series([["xxxjpgzzz.jpg"]])
    tm.assert_series_equal(result, exp)

    # non explicit regex split, pattern length == 1
    result = values.str.split(r".")
    exp = Series([["xxxjpgzzz", "jpg"]])
    tm.assert_series_equal(result, exp)

    # non explicit regex split, pattern length != 1
    result = values.str.split(r".jpg")
    exp = Series([["xx", "zzz", ""]])
    tm.assert_series_equal(result, exp)

    # regex=False with pattern compiled regex raises error
    with pytest.raises(
        ValueError,
        match="Cannot use a compiled regex as replacement pattern with regex=False",
    ):
        values.str.split(regex_pat, regex=False)

