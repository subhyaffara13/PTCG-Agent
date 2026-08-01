
def test_xs(axis, key, dtype):
    single_block = dtype == "int64"
    df = DataFrame(
        {"a": [1, 2, 3], "b": [4, 5, 6], "c": np.array([7, 8, 9], dtype=dtype)}
    )
    df_orig = df.copy()

    result = df.xs(key, axis=axis)

    if axis == 1 or single_block:
        assert np.shares_memory(get_array(df, "a"), get_array(result))
    else:
        assert result._mgr._has_no_reference(0)
    if axis == 0:
        assert result.index is not df.columns
    else:
        assert result.index is not df.index

    result.iloc[0] = 0
    tm.assert_frame_equal(df, df_orig)

