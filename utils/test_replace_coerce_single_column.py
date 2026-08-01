
def test_replace_coerce_single_column():
    df = DataFrame({"a": [1.5, 2, 3], "b": 100.5})
    df_orig = df.copy()

    df2 = df.replace(to_replace=1.5, value="a")
    assert np.shares_memory(get_array(df, "b"), get_array(df2, "b"))
    assert not np.shares_memory(get_array(df, "a"), get_array(df2, "a"))

    df2.loc[0, "b"] = 0.5
    tm.assert_frame_equal(df, df_orig)  # Original is unchanged
    assert not np.shares_memory(get_array(df, "b"), get_array(df2, "b"))

