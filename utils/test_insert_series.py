
def test_insert_series():
    df = DataFrame({"a": [1, 2, 3]})
    ser = Series([1, 2, 3])
    ser_orig = ser.copy()
    df.insert(loc=1, value=ser, column="b")
    assert np.shares_memory(get_array(ser), get_array(df, "b"))
    assert not df._mgr._has_no_reference(1)

    df.iloc[0, 1] = 100
    tm.assert_series_equal(ser, ser_orig)

