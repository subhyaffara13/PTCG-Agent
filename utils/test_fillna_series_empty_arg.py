
def test_fillna_series_empty_arg():
    ser = Series([1, np.nan, 2])
    ser_orig = ser.copy()
    result = ser.fillna({})
    assert np.shares_memory(get_array(ser), get_array(result))

    ser.iloc[0] = 100.5
    tm.assert_series_equal(ser_orig, result)

