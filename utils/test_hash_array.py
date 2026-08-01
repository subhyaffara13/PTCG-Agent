
def test_hash_array(series):
    arr = series.values
    tm.assert_numpy_array_equal(hash_array(arr), hash_array(arr))

