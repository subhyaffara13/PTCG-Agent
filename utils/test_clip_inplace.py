
def test_clip_inplace():
    df = DataFrame({"a": [1.5, 2, 3]})
    arr_a = get_array(df, "a")
    df.clip(lower=2, inplace=True)

    assert np.shares_memory(get_array(df, "a"), arr_a)
    assert df._mgr._has_no_reference(0)

