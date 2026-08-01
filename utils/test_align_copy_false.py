
def test_align_copy_false():
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    df_orig = df.copy()
    df2, df3 = df.align(df)

    assert np.shares_memory(get_array(df, "b"), get_array(df2, "b"))
    assert np.shares_memory(get_array(df, "a"), get_array(df2, "a"))

    df2.loc[0, "a"] = 0
    tm.assert_frame_equal(df, df_orig)  # Original is unchanged

    df3.loc[0, "a"] = 0
    tm.assert_frame_equal(df, df_orig)  # Original is unchanged

