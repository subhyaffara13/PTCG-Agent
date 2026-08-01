
def test_interp_fill_functions_inplace(func, dtype):
    # Check that these takes the same code paths as interpolate
    df = DataFrame({"a": [1, np.nan, 2]}, dtype=dtype)
    df_orig = df.copy()
    arr = get_array(df, "a")
    view = df[:]

    getattr(df, func)(inplace=True)

    # Check that copy was triggered in interpolate and that we don't
    # have any references left
    assert not np.shares_memory(arr, get_array(df, "a"))
    tm.assert_frame_equal(df_orig, view)
    assert df._mgr._has_no_reference(0)
    assert view._mgr._has_no_reference(0)

