
def test_replace_regex_inplace_refs():
    df = DataFrame({"a": ["aaa", "bbb"]})
    df_orig = df.copy()
    view = df[:]
    arr = get_array(df, "a")
    df.replace(to_replace=r"^a.*$", value="new", inplace=True, regex=True)
    assert not np.shares_memory(arr, get_array(df, "a"))
    assert df._mgr._has_no_reference(0)
    tm.assert_frame_equal(view, df_orig)

