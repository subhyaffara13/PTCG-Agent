
def test_drop_on_column():
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [0.1, 0.2, 0.3]})
    df_orig = df.copy()
    df2 = df.drop(columns="a")
    df2._mgr._verify_integrity()

    assert np.shares_memory(get_array(df2, "b"), get_array(df, "b"))
    assert np.shares_memory(get_array(df2, "c"), get_array(df, "c"))
    df2.iloc[0, 0] = 0
    assert not np.shares_memory(get_array(df2, "b"), get_array(df, "b"))
    assert np.shares_memory(get_array(df2, "c"), get_array(df, "c"))
    tm.assert_frame_equal(df, df_orig)

