
def test_concat_frames():
    df = DataFrame({"b": ["a"] * 3}, dtype=object)
    df2 = DataFrame({"a": ["a"] * 3}, dtype=object)
    df_orig = df.copy()
    result = concat([df, df2], axis=1)

    assert np.shares_memory(get_array(result, "b"), get_array(df, "b"))
    assert np.shares_memory(get_array(result, "a"), get_array(df2, "a"))

    result.iloc[0, 0] = "d"
    assert not np.shares_memory(get_array(result, "b"), get_array(df, "b"))
    assert np.shares_memory(get_array(result, "a"), get_array(df2, "a"))

    result.iloc[0, 1] = "d"
    assert not np.shares_memory(get_array(result, "a"), get_array(df2, "a"))
    tm.assert_frame_equal(df, df_orig)

