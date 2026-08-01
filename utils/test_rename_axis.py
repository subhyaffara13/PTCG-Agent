
def test_rename_axis(kwargs):
    df = DataFrame({"a": [1, 2, 3, 4]}, index=Index([1, 2, 3, 4], name="a"))
    df_orig = df.copy()
    df2 = df.rename_axis(**kwargs)
    assert np.shares_memory(get_array(df2, "a"), get_array(df, "a"))

    df2.iloc[0, 0] = 0
    assert not np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    tm.assert_frame_equal(df, df_orig)

