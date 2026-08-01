
def test_where_mask_noop_on_single_column(dtype, val, func):
    df = DataFrame({"a": [1, 2, 3], "b": [-4, -5, -6]}, dtype=dtype)
    df_orig = df.copy()

    result = func(df, val)
    assert np.shares_memory(get_array(df, "b"), get_array(result, "b"))
    assert not np.shares_memory(get_array(df, "a"), get_array(result, "a"))

    result.iloc[0, 1] = 10
    assert not np.shares_memory(get_array(df, "b"), get_array(result, "b"))
    tm.assert_frame_equal(df, df_orig)

