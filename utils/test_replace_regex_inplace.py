
def test_replace_regex_inplace():
    df = DataFrame({"a": ["aaa", "bbb"]})
    arr = get_array(df, "a")
    df.replace(to_replace=r"^a.*$", value="new", inplace=True, regex=True)
    assert df._mgr._has_no_reference(0)
    assert tm.shares_memory(arr, get_array(df, "a"))

    df_orig = df.copy()
    df2 = df.replace(to_replace=r"^b.*$", value="new", regex=True)
    tm.assert_frame_equal(df_orig, df)
    assert not tm.shares_memory(get_array(df2, "a"), get_array(df, "a"))

