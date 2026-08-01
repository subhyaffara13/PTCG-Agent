
def test_setitem_positional_float_into_int_coerces():
    # Case where we hit a KeyError and then trying to set in-place incorrectly
    #  casts a float to an int;
    # As of 3.0 we always treat int keys as labels, so this becomes
    #  setitem-with-expansion
    ser = Series([1, 2, 3], index=["a", "b", "c"])

    ser[0] = 1.5
    expected = Series([1, 2, 3, 1.5], index=["a", "b", "c", 0])
    tm.assert_series_equal(ser, expected)

