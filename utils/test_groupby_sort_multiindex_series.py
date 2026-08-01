
def test_groupby_sort_multiindex_series():
    # series multiindex groupby sort argument was not being passed through
    # _compress_group_index
    # GH 9444
    index = MultiIndex(
        levels=[[1, 2], [1, 2]],
        codes=[[0, 0, 0, 0, 1, 1], [1, 1, 0, 0, 0, 0]],
        names=["a", "b"],
    )
    mseries = Series([0, 1, 2, 3, 4, 5], index=index)
    index = MultiIndex(
        levels=[[1, 2], [1, 2]], codes=[[0, 0, 1], [1, 0, 0]], names=["a", "b"]
    )
    mseries_result = Series([0, 2, 4], index=index)

    result = mseries.groupby(level=["a", "b"], sort=False).first()
    tm.assert_series_equal(result, mseries_result)
    result = mseries.groupby(level=["a", "b"], sort=True).first()
    tm.assert_series_equal(result, mseries_result.sort_index())

