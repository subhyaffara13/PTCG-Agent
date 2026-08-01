
def test_replace_columnwise_no_op():
    df = DataFrame({"a": [1, 2, 3], "b": [1, 2, 3]})
    df_orig = df.copy()
    df2 = df.replace({"a": 10}, 100)
    assert np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    df2.iloc[0, 0] = 100
    tm.assert_frame_equal(df, df_orig)

