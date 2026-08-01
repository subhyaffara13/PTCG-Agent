
def test_transpose_different_dtypes():
    df = DataFrame({"a": [1, 2, 3], "b": 1.5})
    df_orig = df.copy()
    result = df.T

    assert not np.shares_memory(get_array(df, "a"), get_array(result, 0))
    result.iloc[0, 0] = 100
    tm.assert_frame_equal(df, df_orig)

