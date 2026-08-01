
def test_replace_categorical():
    df = DataFrame({"a": Categorical([1, 2, 3])})
    df_orig = df.copy()
    df2 = df.replace(to_replace=1, value=1)

    assert df._mgr._has_no_reference(0)
    assert df2._mgr._has_no_reference(0)
    assert not np.shares_memory(get_array(df, "a").codes, get_array(df2, "a").codes)
    tm.assert_frame_equal(df, df_orig)

    arr_a = get_array(df2, "a").codes
    df2.iloc[0, 0] = 2.0
    assert np.shares_memory(get_array(df2, "a").codes, arr_a)

