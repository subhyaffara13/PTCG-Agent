
def test_astype_numpy_to_ea():
    ser = Series([1, 2, 3])
    result = ser.astype("Int64")
    assert np.shares_memory(get_array(ser), get_array(result))

