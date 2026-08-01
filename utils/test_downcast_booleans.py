
def test_downcast_booleans():
    # see gh-16875: coercing of booleans.
    ser = Series([True, True, False])
    result = maybe_downcast_to_dtype(ser, np.dtype(np.float64))

    expected = ser.values
    tm.assert_numpy_array_equal(result, expected)

