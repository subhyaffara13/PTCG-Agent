
def test_get_with_ea(arr):
    # GH#21260
    ser = Series(arr, index=[2 * i for i in range(len(arr))])
    assert ser.get(4) == ser.iloc[2]

    result = ser.get([4, 6])
    expected = ser.iloc[[2, 3]]
    tm.assert_series_equal(result, expected)

    result = ser.get(slice(2))
    expected = ser.iloc[[0, 1]]
    tm.assert_series_equal(result, expected)

    assert ser.get(-1) is None
    assert ser.get(ser.index.max() + 1) is None

    ser = Series(arr[:6], index=list("abcdef"))
    assert ser.get("c") == ser.iloc[2]

    result = ser.get(slice("b", "d"))
    expected = ser.iloc[[1, 2, 3]]
    tm.assert_series_equal(result, expected)

    result = ser.get("Z")
    assert result is None

    # As of 3.0, ints are treated as labels
    assert ser.get(4) is None
    assert ser.get(-1) is None
    assert ser.get(len(ser)) is None

    # GH#21257
    ser = Series(arr)
    ser2 = ser[::2]
    assert ser2.get(1) is None

