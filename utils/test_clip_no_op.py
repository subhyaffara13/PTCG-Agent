
def test_clip_no_op():
    df = DataFrame({"a": [1.5, 2, 3]})
    df2 = df.clip(lower=0)

    assert not df._mgr._has_no_reference(0)
    assert np.shares_memory(get_array(df2, "a"), get_array(df, "a"))

