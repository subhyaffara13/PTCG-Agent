
def test_sort_index():
    # GH 49473
    ser = Series([1, 2, 3])
    ser_orig = ser.copy()
    ser2 = ser.sort_index()
    assert np.shares_memory(ser.values, ser2.values)

    # mutating ser triggers a copy-on-write for the column / block
    ser2.iloc[0] = 0
    assert not np.shares_memory(ser2.values, ser.values)
    tm.assert_series_equal(ser, ser_orig)

