
def test_non_object_dtype(data):
    ser = pd.Series(data)
    result = ser.explode()
    tm.assert_series_equal(result, ser)

