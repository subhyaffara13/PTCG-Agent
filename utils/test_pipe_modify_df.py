
def test_pipe_modify_df():
    df = DataFrame({"a": [1, 2, 3], "b": 1.5})
    df_orig = df.copy()

    def testfunc(df):
        df.iloc[0, 0] = 100
        return df

    df2 = df.pipe(testfunc)

    assert np.shares_memory(get_array(df2, "b"), get_array(df, "b"))

    tm.assert_frame_equal(df, df_orig)
    assert not np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    assert np.shares_memory(get_array(df2, "b"), get_array(df, "b"))

