
def test_shift_no_op():
    df = DataFrame(
        [[1, 2], [3, 4], [5, 6]],
        index=date_range("2020-01-01", "2020-01-03"),
        columns=["a", "b"],
    )
    df_orig = df.copy()
    df2 = df.shift(periods=0)
    assert np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    assert df2.index is not df.index
    assert df2.columns is not df.columns

    df.iloc[0, 0] = 0
    assert not np.shares_memory(get_array(df, "a"), get_array(df2, "a"))
    assert np.shares_memory(get_array(df, "b"), get_array(df2, "b"))
    tm.assert_frame_equal(df2, df_orig)

