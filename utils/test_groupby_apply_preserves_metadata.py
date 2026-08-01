
def test_groupby_apply_preserves_metadata():
    # GH#62134 - Test that apply() preserves metadata when returning DataFrames/Series
    custom_df = tm.SubclassedDataFrame({"a": [1, 2, 3], "b": [1, 1, 2], "c": [7, 8, 9]})
    custom_df.testattr = "hello"

    def sum_func(group):
        assert isinstance(group, tm.SubclassedDataFrame)
        assert hasattr(group, "testattr")
        assert group.testattr == "hello"
        return group.sum()

    result = custom_df.groupby("c").apply(sum_func)
    assert hasattr(result, "testattr"), "DataFrame apply() should preserve metadata"
    assert result.testattr == "hello"

    custom_series = tm.SubclassedSeries([1, 2, 3])
    custom_series.testattr = "hello"

    def sum_series_func(group):
        assert isinstance(group, tm.SubclassedSeries)
        assert hasattr(group, "testattr")
        assert group.testattr == "hello"
        return group.sum()

    result = custom_series.groupby(custom_df["c"]).apply(sum_series_func)
    assert hasattr(result, "testattr"), "Series apply() should preserve metadata"
    assert result.testattr == "hello"

