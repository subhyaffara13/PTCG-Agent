
def test_clip_inplace_reference_no_op():
    df = DataFrame({"a": [1.5, 2, 3]})
    df_copy = df.copy()
    arr_a = get_array(df, "a")
    view = df[:]
    df.clip(lower=0, inplace=True)

    assert np.shares_memory(get_array(df, "a"), arr_a)

    assert not df._mgr._has_no_reference(0)
    assert not view._mgr._has_no_reference(0)
    tm.assert_frame_equal(df_copy, view)

