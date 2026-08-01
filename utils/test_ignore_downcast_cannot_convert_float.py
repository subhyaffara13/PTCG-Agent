
def test_ignore_downcast_cannot_convert_float(data, expected, downcast):
    # Cannot cast to an integer (signed or unsigned)
    # because we have a float number.
    res = to_numeric(data, downcast=downcast)
    tm.assert_numpy_array_equal(res, expected)

