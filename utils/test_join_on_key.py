
def test_join_on_key(dtype):
    df_index = Index(["a", "b", "c"], name="key", dtype=dtype)

    df1 = DataFrame({"a": [1, 2, 3]}, index=df_index.copy(deep=True))
    df2 = DataFrame({"b": [4, 5, 6]}, index=df_index.copy(deep=True))

    df1_orig = df1.copy()
    df2_orig = df2.copy()

    result = df1.join(df2, on="key")

    assert np.shares_memory(get_array(result, "a"), get_array(df1, "a"))
    assert np.shares_memory(get_array(result, "b"), get_array(df2, "b"))
    assert tm.shares_memory(get_array(result.index), get_array(df1.index))
    assert not np.shares_memory(get_array(result.index), get_array(df2.index))

    result.iloc[0, 0] = 0
    assert not np.shares_memory(get_array(result, "a"), get_array(df1, "a"))
    assert np.shares_memory(get_array(result, "b"), get_array(df2, "b"))

    result.iloc[0, 1] = 0
    assert not np.shares_memory(get_array(result, "b"), get_array(df2, "b"))

    tm.assert_frame_equal(df1, df1_orig)
    tm.assert_frame_equal(df2, df2_orig)

