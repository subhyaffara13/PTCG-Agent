
def test_explode_sets():
    # https://github.com/pandas-dev/pandas/issues/35614
    s = pd.Series([{"a", "b", "c"}], index=[1])
    result = s.explode().sort_values()
    expected = pd.Series(["a", "b", "c"], index=[1, 1, 1])
    tm.assert_series_equal(result, expected)


def test_explode_sets():
    # https://github.com/pandas-dev/pandas/issues/35614
    df = pd.DataFrame({"a": [{"x", "y"}], "b": [1]}, index=[1])
    result = df.explode(column="a").sort_values(by="a")
    expected = pd.DataFrame({"a": ["x", "y"], "b": [1, 1]}, index=[1, 1])
    tm.assert_frame_equal(result, expected)

