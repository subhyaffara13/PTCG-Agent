
def test_series_reorder_levels():
    index = MultiIndex.from_tuples(
        [(1, 1), (1, 2), (2, 1), (2, 2)], names=["one", "two"]
    )
    ser = Series([1, 2, 3, 4], index=index)
    ser_orig = ser.copy()
    ser2 = ser.reorder_levels(order=["two", "one"])
    assert np.shares_memory(ser2.values, ser.values)

    ser2.iloc[0] = 0
    assert not np.shares_memory(ser2.values, ser.values)
    tm.assert_series_equal(ser, ser_orig)

