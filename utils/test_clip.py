
def test_clip():
    df = DataFrame({"a": [1.5, 2, 3]})
    df_orig = df.copy()
    df2 = df.clip(lower=2)

    assert not np.shares_memory(get_array(df2, "a"), get_array(df, "a"))

    assert df._mgr._has_no_reference(0)
    tm.assert_frame_equal(df_orig, df)

