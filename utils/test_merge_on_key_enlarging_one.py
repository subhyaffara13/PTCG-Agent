
def test_merge_on_key_enlarging_one(func, how):
    df1 = DataFrame({"key": Series(["a", "b", "c"], dtype=object), "a": [1, 2, 3]})
    df2 = DataFrame({"key": Series(["a", "b"], dtype=object), "b": [4, 5]})
    df1_orig = df1.copy()
    df2_orig = df2.copy()

    result = func(df1, df2, how=how)

    assert np.shares_memory(get_array(result, "a"), get_array(df1, "a"))
    assert not np.shares_memory(get_array(result, "b"), get_array(df2, "b"))
    assert df2._mgr._has_no_reference(1)
    assert df2._mgr._has_no_reference(0)
    assert np.shares_memory(get_array(result, "key"), get_array(df1, "key")) is (
        how == "left"
    )
    assert not np.shares_memory(get_array(result, "key"), get_array(df2, "key"))

    if how == "left":
        result.iloc[0, 1] = 0
    else:
        result.iloc[0, 2] = 0
    assert not np.shares_memory(get_array(result, "a"), get_array(df1, "a"))
    tm.assert_frame_equal(df1, df1_orig)
    tm.assert_frame_equal(df2, df2_orig)

