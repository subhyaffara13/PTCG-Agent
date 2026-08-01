
def test_align_with_series_copy_false():
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    ser = Series([1, 2, 3], name="x")
    ser_orig = ser.copy()
    df_orig = df.copy()
    df2, ser2 = df.align(ser, axis=0)

    assert np.shares_memory(get_array(df, "b"), get_array(df2, "b"))
    assert np.shares_memory(get_array(df, "a"), get_array(df2, "a"))
    assert np.shares_memory(get_array(ser, "x"), get_array(ser2, "x"))

    df2.loc[0, "a"] = 0
    tm.assert_frame_equal(df, df_orig)  # Original is unchanged

    ser2.loc[0] = 0
    tm.assert_series_equal(ser, ser_orig)  # Original is unchanged

