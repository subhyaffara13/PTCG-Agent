
def test_asfreq_noop():
    df = DataFrame(
        {"a": [0.0, None, 2.0, 3.0]},
        index=date_range("1/1/2000", periods=4, freq="min"),
    )
    df_orig = df.copy()
    df2 = df.asfreq(freq="min")
    assert np.shares_memory(get_array(df2, "a"), get_array(df, "a"))

    # mutating df2 triggers a copy-on-write for that column / block
    df2.iloc[0, 0] = 0

    assert not np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    tm.assert_frame_equal(df, df_orig)

