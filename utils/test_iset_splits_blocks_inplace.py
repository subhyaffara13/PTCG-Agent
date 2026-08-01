
def test_iset_splits_blocks_inplace(locs, arr, dtype):
    # Nothing currently calls iset with
    # more than 1 loc with inplace=True (only happens with inplace=False)
    # but ensure that it works
    df = DataFrame(
        {
            "a": [1, 2, 3],
            "b": [4, 5, 6],
            "c": [7, 8, 9],
            "d": [10, 11, 12],
            "e": [13, 14, 15],
            "f": Series(["a", "b", "c"], dtype=object),
        },
    )
    arr = arr.astype(dtype)
    df_orig = df.copy()
    df2 = df.copy(deep=False)  # Trigger a CoW (if enabled, otherwise makes copy)
    df2._mgr.iset(locs, arr, inplace=True)

    tm.assert_frame_equal(df, df_orig)
    for i, col in enumerate(df.columns):
        if i not in locs:
            assert np.shares_memory(get_array(df, col), get_array(df2, col))

