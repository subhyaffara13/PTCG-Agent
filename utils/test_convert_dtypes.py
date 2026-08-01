
def test_convert_dtypes(using_infer_string):
    df = DataFrame({"a": ["a", "b"], "b": [1, 2], "c": [1.5, 2.5], "d": [True, False]})
    df_orig = df.copy()
    df2 = df.convert_dtypes()

    if using_infer_string:
        # String column is already Arrow-backed, so memory is shared
        assert tm.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    else:
        # String column converts from object to Arrow, no memory sharing
        assert not tm.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    assert tm.shares_memory(get_array(df2, "d"), get_array(df, "d"))
    assert tm.shares_memory(get_array(df2, "b"), get_array(df, "b"))
    assert tm.shares_memory(get_array(df2, "c"), get_array(df, "c"))
    df2.iloc[0, 0] = "x"
    df2.iloc[0, 1] = 10
    tm.assert_frame_equal(df, df_orig)

