
def test_merge_on_key(func):
    df1 = DataFrame({"key": Series(["a", "b", "c"], dtype=object), "a": [1, 2, 3]})
    df2 = DataFrame({"key": Series(["a", "b", "c"], dtype=object), "b": [4, 5, 6]})
    df1_orig = df1.copy()
    df2_orig = df2.copy()

    result = func(df1, df2, on="key")

    assert np.shares_memory(get_array(result, "a"), get_array(df1, "a"))
    assert np.shares_memory(get_array(result, "b"), get_array(df2, "b"))
    assert np.shares_memory(get_array(result, "key"), get_array(df1, "key"))
    assert not np.shares_memory(get_array(result, "key"), get_array(df2, "key"))

    result.iloc[0, 1] = 0
    assert not np.shares_memory(get_array(result, "a"), get_array(df1, "a"))
    assert np.shares_memory(get_array(result, "b"), get_array(df2, "b"))

    result.iloc[0, 2] = 0
    assert not np.shares_memory(get_array(result, "b"), get_array(df2, "b"))
    tm.assert_frame_equal(df1, df1_orig)
    tm.assert_frame_equal(df2, df2_orig)

