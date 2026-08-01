
def test_isetitem():
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]})
    df_orig = df.copy()
    df2 = df.copy(deep=False)  # Trigger a CoW
    df2.isetitem(1, np.array([-1, -2, -3]))  # This is inplace
    assert np.shares_memory(get_array(df, "c"), get_array(df2, "c"))
    assert np.shares_memory(get_array(df, "a"), get_array(df2, "a"))

    df2.loc[0, "a"] = 0
    tm.assert_frame_equal(df, df_orig)  # Original is unchanged
    assert np.shares_memory(get_array(df, "c"), get_array(df2, "c"))

