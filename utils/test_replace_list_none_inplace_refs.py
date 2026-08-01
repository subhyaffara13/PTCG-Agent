
def test_replace_list_none_inplace_refs():
    df = DataFrame({"a": ["a", "b", "c"]})
    arr = get_array(df, "a")
    df_orig = df.copy()
    view = df[:]
    df.replace(["a"], value=None, inplace=True)
    assert df._mgr._has_no_reference(0)
    assert not np.shares_memory(arr, get_array(df, "a"))
    tm.assert_frame_equal(df_orig, view)

