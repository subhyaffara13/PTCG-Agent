
def test_loc_mixed_int_float():
    # GH#19456
    ser = Series(range(2), Index([1, 2.0], dtype=object))

    result = ser.loc[1]
    assert result == 0

