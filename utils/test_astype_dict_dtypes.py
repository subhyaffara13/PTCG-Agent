
def test_astype_dict_dtypes():
    df = DataFrame(
        {"a": [1, 2, 3], "b": [4, 5, 6], "c": Series([1.5, 1.5, 1.5], dtype="float64")}
    )
    df_orig = df.copy()
    df2 = df.astype({"a": "float64", "c": "float64"})

    assert np.shares_memory(get_array(df2, "c"), get_array(df, "c"))
    assert np.shares_memory(get_array(df2, "b"), get_array(df, "b"))
    assert not np.shares_memory(get_array(df2, "a"), get_array(df, "a"))

    # mutating df2 triggers a copy-on-write for that column/block
    df2.iloc[0, 2] = 5.5
    assert not np.shares_memory(get_array(df2, "c"), get_array(df, "c"))

    df2.iloc[0, 1] = 10
    assert not np.shares_memory(get_array(df2, "b"), get_array(df, "b"))
    tm.assert_frame_equal(df, df_orig)

