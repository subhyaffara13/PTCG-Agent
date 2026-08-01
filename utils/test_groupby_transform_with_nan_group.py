
def test_groupby_transform_with_nan_group():
    # GH 9941
    df = DataFrame({"a": range(10), "b": [1, 1, 2, 3, np.nan, 4, 4, 5, 5, 5]})
    result = df.groupby(df.b)["a"].transform(max)
    expected = Series([1.0, 1.0, 2.0, 3.0, np.nan, 6.0, 6.0, 9.0, 9.0, 9.0], name="a")
    tm.assert_series_equal(result, expected)

