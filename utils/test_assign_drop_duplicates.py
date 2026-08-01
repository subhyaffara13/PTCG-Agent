
def test_assign_drop_duplicates(method):
    df = DataFrame({"a": [1, 2, 3]})
    df_orig = df.copy()
    df2 = getattr(df, method)()
    df2._mgr._verify_integrity()

    assert np.shares_memory(get_array(df2, "a"), get_array(df, "a"))

    df2.iloc[0, 0] = 0
    assert not np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    tm.assert_frame_equal(df, df_orig)

