
def test_replace_list_categorical():
    df = DataFrame({"a": ["a", "b", "c"]}, dtype="category")
    arr = get_array(df, "a")

    df.replace(["c"], value="a", inplace=True)
    assert np.shares_memory(arr.codes, get_array(df, "a").codes)
    assert df._mgr._has_no_reference(0)

    df_orig = df.copy()
    df.replace(["b"], value="a")
    df2 = df.apply(lambda x: x.cat.rename_categories({"b": "d"}))
    assert not np.shares_memory(arr.codes, get_array(df2, "a").codes)

    tm.assert_frame_equal(df, df_orig)

