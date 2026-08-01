
def test_replace_listlike_inplace():
    df = DataFrame({"a": [1, 2, 3], "b": [1, 2, 3]})
    arr = get_array(df, "a")
    df.replace([200, 2], [10, 11], inplace=True)
    assert np.shares_memory(get_array(df, "a"), arr)

    view = df[:]
    df_orig = df.copy()
    df.replace([200, 3], [10, 11], inplace=True)
    assert not np.shares_memory(get_array(df, "a"), arr)
    tm.assert_frame_equal(view, df_orig)

