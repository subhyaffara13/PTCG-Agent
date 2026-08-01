
def test_reindex_columns():
    # Case: reindexing the column returns a new dataframe
    # + afterwards modifying the result
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [0.1, 0.2, 0.3]})
    df_orig = df.copy()
    df2 = df.reindex(columns=["a", "c"])

    # still shares memory (df2 is a shallow copy)
    assert np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    # mutating df2 triggers a copy-on-write for that column
    df2.iloc[0, 0] = 0
    assert not np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    assert np.shares_memory(get_array(df2, "c"), get_array(df, "c"))
    tm.assert_frame_equal(df, df_orig)

