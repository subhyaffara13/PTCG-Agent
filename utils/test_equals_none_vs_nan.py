
def test_equals_none_vs_nan():
    # GH#39650
    ser = Series([1, None], dtype=object)
    ser2 = Series([1, np.nan], dtype=object)

    assert ser.equals(ser2)
    assert Index(ser, dtype=ser.dtype).equals(Index(ser2, dtype=ser2.dtype))
    assert ser.array.equals(ser2.array)

