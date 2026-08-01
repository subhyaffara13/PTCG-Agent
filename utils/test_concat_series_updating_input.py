
def test_concat_series_updating_input():
    ser = Series([1, 2], name="a")
    ser2 = Series([3, 4], name="b")
    expected = DataFrame({"a": [1, 2], "b": [3, 4]})
    result = concat([ser, ser2], axis=1)

    assert np.shares_memory(get_array(result, "a"), get_array(ser, "a"))
    assert np.shares_memory(get_array(result, "b"), get_array(ser2, "b"))

    ser.iloc[0] = 100
    assert not np.shares_memory(get_array(result, "a"), get_array(ser, "a"))
    assert np.shares_memory(get_array(result, "b"), get_array(ser2, "b"))
    tm.assert_frame_equal(result, expected)

    ser2.iloc[0] = 1000
    assert not np.shares_memory(get_array(result, "b"), get_array(ser2, "b"))
    tm.assert_frame_equal(result, expected)

