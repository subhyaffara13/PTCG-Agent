
def test_eval_inplace():
    df = DataFrame({"a": [1, 2, 3], "b": 1})
    df_orig = df.copy()
    df_view = df[:]

    df.eval("c = a+b", inplace=True)
    assert np.shares_memory(get_array(df, "a"), get_array(df_view, "a"))

    df.iloc[0, 0] = 100
    tm.assert_frame_equal(df_view, df_orig)

