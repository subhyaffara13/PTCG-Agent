
def test_droplevel():
    # GH 49473
    index = MultiIndex.from_tuples([(1, 1), (1, 2), (2, 1)], names=["one", "two"])
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]}, index=index)
    df_orig = df.copy()
    df2 = df.droplevel(0)

    assert np.shares_memory(get_array(df2, "c"), get_array(df, "c"))
    assert np.shares_memory(get_array(df2, "a"), get_array(df, "a"))

    # mutating df2 triggers a copy-on-write for that column / block
    df2.iloc[0, 0] = 0

    assert not np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    assert np.shares_memory(get_array(df2, "b"), get_array(df, "b"))

    tm.assert_frame_equal(df, df_orig)

