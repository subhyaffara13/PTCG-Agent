
def test_split_regex(any_string_dtype):
    # GH 43563
    # explicit regex = True split
    values = Series("xxxjpgzzz.jpg", dtype=any_string_dtype)
    result = values.str.split(r"\.jpg", regex=True)
    exp = Series([["xxxjpgzzz", ""]])
    tm.assert_series_equal(result, exp)

