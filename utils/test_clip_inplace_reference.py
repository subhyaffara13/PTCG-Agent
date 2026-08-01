
def test_clip_inplace_reference():
    df = DataFrame({"a": [1.5, 2, 3]})
    df_copy = df.copy()
    arr_a = get_array(df, "a")
    view = df[:]
    df.clip(lower=2, inplace=True)

    assert not np.shares_memory(get_array(df, "a"), arr_a)
    assert df._mgr._has_no_reference(0)
    assert view._mgr._has_no_reference(0)
    tm.assert_frame_equal(df_copy, view)

