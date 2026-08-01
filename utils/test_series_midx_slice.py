
def test_series_midx_slice():
    ser = Series([1, 2, 3], index=pd.MultiIndex.from_arrays([[1, 1, 2], [3, 4, 5]]))
    ser_orig = ser.copy()
    result = ser[1]
    assert np.shares_memory(get_array(ser), get_array(result))
    result.iloc[0] = 100
    tm.assert_series_equal(ser, ser_orig)

