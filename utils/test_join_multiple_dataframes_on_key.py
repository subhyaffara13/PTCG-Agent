
def test_join_multiple_dataframes_on_key():
    df_index = Index(["a", "b", "c"], name="key", dtype=object)

    df1 = DataFrame({"a": [1, 2, 3]}, index=df_index.copy(deep=True))
    dfs_list = [
        DataFrame({"b": [4, 5, 6]}, index=df_index.copy(deep=True)),
        DataFrame({"c": [7, 8, 9]}, index=df_index.copy(deep=True)),
    ]

    df1_orig = df1.copy()
    dfs_list_orig = [df.copy() for df in dfs_list]

    result = df1.join(dfs_list)

    assert np.shares_memory(get_array(result, "a"), get_array(df1, "a"))
    assert np.shares_memory(get_array(result, "b"), get_array(dfs_list[0], "b"))
    assert np.shares_memory(get_array(result, "c"), get_array(dfs_list[1], "c"))
    assert np.shares_memory(get_array(result.index), get_array(df1.index))
    assert not np.shares_memory(get_array(result.index), get_array(dfs_list[0].index))
    assert not np.shares_memory(get_array(result.index), get_array(dfs_list[1].index))

    result.iloc[0, 0] = 0
    assert not np.shares_memory(get_array(result, "a"), get_array(df1, "a"))
    assert np.shares_memory(get_array(result, "b"), get_array(dfs_list[0], "b"))
    assert np.shares_memory(get_array(result, "c"), get_array(dfs_list[1], "c"))

    result.iloc[0, 1] = 0
    assert not np.shares_memory(get_array(result, "b"), get_array(dfs_list[0], "b"))
    assert np.shares_memory(get_array(result, "c"), get_array(dfs_list[1], "c"))

    result.iloc[0, 2] = 0
    assert not np.shares_memory(get_array(result, "c"), get_array(dfs_list[1], "c"))

    tm.assert_frame_equal(df1, df1_orig)
    for df, df_orig in zip(dfs_list, dfs_list_orig, strict=True):
        tm.assert_frame_equal(df, df_orig)

