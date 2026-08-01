
def test_putmask(dtype):
    df = DataFrame({"a": [1, 2], "b": 1, "c": 2}, dtype=dtype)
    view = df[:]
    df_orig = df.copy()
    df[df == df] = 5

    assert not np.shares_memory(get_array(view, "a"), get_array(df, "a"))
    tm.assert_frame_equal(view, df_orig)

