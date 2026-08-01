
def test_getitem_midx_slice():
    df = DataFrame({("a", "x"): [1, 2], ("a", "y"): 1, ("b", "x"): 2})
    df_orig = df.copy()
    new_df = df[("a",)]

    assert not new_df._mgr._has_no_reference(0)

    assert np.shares_memory(get_array(df, ("a", "x")), get_array(new_df, "x"))
    new_df.iloc[0, 0] = 100
    tm.assert_frame_equal(df_orig, df)

