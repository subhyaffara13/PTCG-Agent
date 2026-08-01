
def test_shift_rows_freq():
    df = DataFrame(
        [[1, 2], [3, 4], [5, 6]],
        index=date_range("2020-01-01", "2020-01-03"),
        columns=["a", "b"],
    )
    df_orig = df.copy()
    df_orig.index = date_range("2020-01-02", "2020-01-04")
    df2 = df.shift(periods=1, freq="1D")

    assert np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    df.iloc[0, 0] = 0
    assert not np.shares_memory(get_array(df, "a"), get_array(df2, "a"))
    tm.assert_frame_equal(df2, df_orig)

