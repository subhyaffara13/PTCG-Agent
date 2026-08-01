
def test_str_accessor_in_apply_func():
    # https://github.com/pandas-dev/pandas/issues/38979
    df = DataFrame(zip("abc", "def", strict=True))
    expected = Series(["A/D", "B/E", "C/F"])
    result = df.apply(lambda f: "/".join(f.str.upper()), axis=1)
    tm.assert_series_equal(result, expected)

