
def test_replace_to_replace_wrong_dtype():
    df = DataFrame({"a": [1.5, 2, 3], "b": 100.5})
    df_orig = df.copy()

    df2 = df.replace(to_replace="xxx", value=1.5)

    assert np.shares_memory(get_array(df, "b"), get_array(df2, "b"))
    assert np.shares_memory(get_array(df, "a"), get_array(df2, "a"))

    df2.loc[0, "b"] = 0.5
    tm.assert_frame_equal(df, df_orig)  # Original is unchanged
    assert not np.shares_memory(get_array(df, "b"), get_array(df2, "b"))

