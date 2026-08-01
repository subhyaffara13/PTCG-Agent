
def test_replace_list_none():
    df = DataFrame({"a": ["a", "b", "c"]})

    df_orig = df.copy()
    df2 = df.replace(["b"], value=None)
    tm.assert_frame_equal(df, df_orig)

    assert not np.shares_memory(get_array(df, "a"), get_array(df2, "a"))

    # replace multiple values that don't actually replace anything with None
    # https://github.com/pandas-dev/pandas/issues/59770
    df3 = df.replace(["d", "e", "f"], value=None)
    tm.assert_frame_equal(df3, df_orig)
    assert tm.shares_memory(get_array(df, "a"), get_array(df3, "a"))

