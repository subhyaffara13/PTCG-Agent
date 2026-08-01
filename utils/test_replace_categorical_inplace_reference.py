
def test_replace_categorical_inplace_reference(to_replace):
    df = DataFrame({"a": Categorical([1, 2, 3])})
    df_orig = df.copy()
    arr_a = get_array(df, "a")
    view = df[:]
    df.replace(to_replace=to_replace, value=1, inplace=True)
    assert not np.shares_memory(get_array(df, "a").codes, arr_a.codes)
    assert df._mgr._has_no_reference(0)
    assert view._mgr._has_no_reference(0)
    tm.assert_frame_equal(view, df_orig)

