
def test_replace_mask_all_false_second_block():
    df = DataFrame({"a": [1.5, 2, 3], "b": 100.5, "c": 1, "d": 2})
    df_orig = df.copy()

    df2 = df.replace(to_replace=1.5, value=55.5)

    # TODO: Block splitting would allow us to avoid copying b
    assert np.shares_memory(get_array(df, "c"), get_array(df2, "c"))
    assert not np.shares_memory(get_array(df, "a"), get_array(df2, "a"))

    df2.loc[0, "c"] = 1
    tm.assert_frame_equal(df, df_orig)  # Original is unchanged

    assert not np.shares_memory(get_array(df, "c"), get_array(df2, "c"))
    assert np.shares_memory(get_array(df, "d"), get_array(df2, "d"))

