
def test_group_diff_datetimelike(data, unit):
    df = DataFrame({"a": [1, 2, 2], "b": data})
    df["b"] = df["b"].dt.as_unit(unit)
    result = df.groupby("a")["b"].diff()
    expected = Series([NaT, NaT, Timedelta("1 days")], name="b").dt.as_unit(unit)
    tm.assert_series_equal(result, expected)

