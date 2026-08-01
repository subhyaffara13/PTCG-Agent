
def test_fillna_inplace_ea_noop_shares_memory(any_numeric_ea_and_arrow_dtype):
    df = DataFrame({"a": [1, NA, 3], "b": 1}, dtype=any_numeric_ea_and_arrow_dtype)
    df_orig = df.copy()
    view = df[:]
    df.fillna(100, inplace=True)
    assert not np.shares_memory(get_array(df, "a"), get_array(view, "a"))

    assert np.shares_memory(get_array(df, "b"), get_array(view, "b"))
    assert not df._mgr._has_no_reference(1)
    assert not view._mgr._has_no_reference(1)

    df.iloc[0, 1] = 100
    tm.assert_frame_equal(df_orig, view)

