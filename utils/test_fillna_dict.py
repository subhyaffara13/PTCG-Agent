
def test_fillna_dict():
    df = DataFrame({"a": [1.5, np.nan], "b": 1})
    df_orig = df.copy()

    df2 = df.fillna({"a": 100.5})
    assert np.shares_memory(get_array(df, "b"), get_array(df2, "b"))
    assert not np.shares_memory(get_array(df, "a"), get_array(df2, "a"))

    df2.iloc[0, 1] = 100
    tm.assert_frame_equal(df_orig, df)

