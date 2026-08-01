
def test_xs_multiindex(key, level, axis):
    arr = np.arange(18).reshape(6, 3)
    index = MultiIndex.from_product([["l1", "l2"], [1, 2, 3]], names=["lev1", "lev2"])
    df = DataFrame(arr, index=index, columns=list("abc"))
    if axis == 1:
        df = df.transpose().copy()
    df_orig = df.copy()

    result = df.xs(key, level=level, axis=axis)

    if level == 0:
        assert np.shares_memory(
            get_array(df, df.columns[0]), get_array(result, result.columns[0])
        )
    assert result.index is not df.index
    assert result.columns is not df.columns

    result.iloc[0, 0] = 0
    tm.assert_frame_equal(df, df_orig)

