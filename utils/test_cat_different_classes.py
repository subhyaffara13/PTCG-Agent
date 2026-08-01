
def test_cat_different_classes(klass):
    # https://github.com/pandas-dev/pandas/issues/33425
    s = Series(["a", "b", "c"])
    result = s.str.cat(klass(["x", "y", "z"]))
    expected = Series(["ax", "by", "cz"])
    tm.assert_series_equal(result, expected)

