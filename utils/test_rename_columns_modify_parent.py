
def test_rename_columns_modify_parent():
    # Case: renaming columns returns a new dataframe
    # + afterwards modifying the original (parent) dataframe
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [0.1, 0.2, 0.3]})
    df2 = df.rename(columns=str.upper)
    df2_orig = df2.copy()

    assert np.shares_memory(get_array(df2, "A"), get_array(df, "a"))
    df.iloc[0, 0] = 0
    assert not np.shares_memory(get_array(df2, "A"), get_array(df, "a"))
    assert np.shares_memory(get_array(df2, "C"), get_array(df, "c"))
    expected = DataFrame({"a": [0, 2, 3], "b": [4, 5, 6], "c": [0.1, 0.2, 0.3]})
    tm.assert_frame_equal(df, expected)
    tm.assert_frame_equal(df2, df2_orig)

