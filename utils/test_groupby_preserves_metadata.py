
def test_groupby_preserves_metadata():
    # GH-37343
    custom_df = tm.SubclassedDataFrame({"a": [1, 2, 3], "b": [1, 1, 2], "c": [7, 8, 9]})
    assert "testattr" in custom_df._metadata
    custom_df.testattr = "hello"
    for _, group_df in custom_df.groupby("c"):
        assert group_df.testattr == "hello"

    # GH-45314
    def func(group):
        assert isinstance(group, tm.SubclassedDataFrame)
        assert hasattr(group, "testattr")
        assert group.testattr == "hello"
        return group.testattr

    result = custom_df.groupby("c").apply(func)
    expected = tm.SubclassedSeries(["hello"] * 3, index=Index([7, 8, 9], name="c"))
    tm.assert_series_equal(result, expected)

    result = custom_df.groupby("c").apply(func)
    tm.assert_series_equal(result, expected)

    # https://github.com/pandas-dev/pandas/pull/56761
    result = custom_df.groupby("c")[["a", "b"]].apply(func)
    tm.assert_series_equal(result, expected)

    def func2(group):
        assert isinstance(group, tm.SubclassedSeries)
        assert hasattr(group, "testattr")
        return group.testattr

    custom_series = tm.SubclassedSeries([1, 2, 3])
    custom_series.testattr = "hello"
    result = custom_series.groupby(custom_df["c"]).apply(func2)
    tm.assert_series_equal(result, expected)
    result = custom_series.groupby(custom_df["c"]).agg(func2)
    tm.assert_series_equal(result, expected)

