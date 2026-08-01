
def test_subset_chained_single_block_row():
    # not parametrizing this for dtype backend, since this explicitly tests single block
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]})
    df_orig = df.copy()

    # modify subset -> don't modify parent
    subset = df[:].iloc[0].iloc[0:2]
    subset.iloc[0] = 0
    tm.assert_frame_equal(df, df_orig)

    # modify parent -> don't modify subset
    subset = df[:].iloc[0].iloc[0:2]
    df.iloc[0, 0] = 0
    expected = Series([1, 4], index=["a", "b"], name=0)
    tm.assert_series_equal(subset, expected)

