
def test_replace_columnwise_no_op_inplace():
    df = DataFrame({"a": [1, 2, 3], "b": [1, 2, 3]})
    view = df[:]
    df_orig = df.copy()
    df.replace({"a": 10}, 100, inplace=True)
    assert np.shares_memory(get_array(view, "a"), get_array(df, "a"))
    df.iloc[0, 0] = 100
    tm.assert_frame_equal(view, df_orig)

