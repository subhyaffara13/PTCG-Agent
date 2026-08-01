
def test_interpolate_inplace_with_refs(vals):
    df = DataFrame({"a": [1, np.nan, 2]})
    df_orig = df.copy()
    arr = get_array(df, "a")
    view = df[:]
    df.interpolate(method="linear", inplace=True)
    # Check that copy was triggered in interpolate and that we don't
    # have any references left
    assert not np.shares_memory(arr, get_array(df, "a"))
    tm.assert_frame_equal(df_orig, view)
    assert df._mgr._has_no_reference(0)
    assert view._mgr._has_no_reference(0)

