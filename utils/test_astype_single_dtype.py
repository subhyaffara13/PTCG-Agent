
def test_astype_single_dtype():
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": 1.5})
    df_orig = df.copy()
    df2 = df.astype("float64")

    assert np.shares_memory(get_array(df2, "c"), get_array(df, "c"))
    assert not np.shares_memory(get_array(df2, "a"), get_array(df, "a"))

    # mutating df2 triggers a copy-on-write for that column/block
    df2.iloc[0, 2] = 5.5
    assert not np.shares_memory(get_array(df2, "c"), get_array(df, "c"))
    tm.assert_frame_equal(df, df_orig)

    # mutating parent also doesn't update result
    df2 = df.astype("float64")
    df.iloc[0, 2] = 5.5
    tm.assert_frame_equal(df2, df_orig.astype("float64"))

