
def test_interp_fill_functions(func):
    # Check that these takes the same code paths as interpolate
    df = DataFrame({"a": [1, 2]})
    df_orig = df.copy()

    result = getattr(df, func)()

    assert np.shares_memory(get_array(result, "a"), get_array(df, "a"))
    assert result.index is not df.index
    assert result.columns is not df.columns

    result.iloc[0, 0] = 100
    assert not np.shares_memory(get_array(result, "a"), get_array(df, "a"))
    tm.assert_frame_equal(df, df_orig)

