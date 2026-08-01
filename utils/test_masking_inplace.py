
def test_masking_inplace(method):
    df = DataFrame({"a": [1.5, 2, 3]})
    df_orig = df.copy()
    arr_a = get_array(df, "a")
    view = df[:]

    method = getattr(df, method)
    method(df["a"] > 1.6, -1, inplace=True)

    assert not np.shares_memory(get_array(df, "a"), arr_a)
    assert df._mgr._has_no_reference(0)
    assert view._mgr._has_no_reference(0)
    tm.assert_frame_equal(view, df_orig)

