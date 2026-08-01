
def test_head_tail(method):
    df = DataFrame({"a": [1, 2, 3], "b": [0.1, 0.2, 0.3]})
    df_orig = df.copy()
    df2 = method(df)
    df2._mgr._verify_integrity()

    # We are explicitly deviating for CoW here to make an eager copy (avoids
    # tracking references for very cheap ops)
    assert not np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    assert not np.shares_memory(get_array(df2, "b"), get_array(df, "b"))

    # modify df2 to trigger CoW for that block
    df2.iloc[0, 0] = 0
    assert not np.shares_memory(get_array(df2, "b"), get_array(df, "b"))
    assert not np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    tm.assert_frame_equal(df, df_orig)


def test_head_tail(string_series):
    tm.assert_series_equal(string_series.head(), string_series[:5])
    tm.assert_series_equal(string_series.head(0), string_series[0:0])
    tm.assert_series_equal(string_series.tail(), string_series[-5:])
    tm.assert_series_equal(string_series.tail(0), string_series[0:0])


def test_head_tail(float_frame):
    tm.assert_frame_equal(float_frame.head(), float_frame[:5])
    tm.assert_frame_equal(float_frame.tail(), float_frame[-5:])

    tm.assert_frame_equal(float_frame.head(0), float_frame[0:0])
    tm.assert_frame_equal(float_frame.tail(0), float_frame[0:0])

    tm.assert_frame_equal(float_frame.head(-1), float_frame[:-1])
    tm.assert_frame_equal(float_frame.tail(-1), float_frame[1:])
    tm.assert_frame_equal(float_frame.head(1), float_frame[:1])
    tm.assert_frame_equal(float_frame.tail(1), float_frame[-1:])
    # with a float index
    df = float_frame.copy()
    df.index = np.arange(len(float_frame)) + 0.1
    tm.assert_frame_equal(df.head(), df.iloc[:5])
    tm.assert_frame_equal(df.tail(), df.iloc[-5:])
    tm.assert_frame_equal(df.head(0), df[0:0])
    tm.assert_frame_equal(df.tail(0), df[0:0])
    tm.assert_frame_equal(df.head(-1), df.iloc[:-1])
    tm.assert_frame_equal(df.tail(-1), df.iloc[1:])

