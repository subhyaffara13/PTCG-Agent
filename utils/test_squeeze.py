
def test_squeeze():
    df = DataFrame({"a": [1, 2, 3]})
    df_orig = df.copy()
    series = df.squeeze()

    # Should share memory regardless of CoW since squeeze is just an iloc
    assert np.shares_memory(series.values, get_array(df, "a"))

    # mutating squeezed df triggers a copy-on-write for that column/block
    series.iloc[0] = 0
    assert not np.shares_memory(series.values, get_array(df, "a"))
    tm.assert_frame_equal(df, df_orig)

