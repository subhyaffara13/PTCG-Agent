
def test_getitem_1tuple_slice_without_multiindex():
    ser = Series(range(5))
    key = (slice(3),)

    result = ser[key]
    expected = ser[key[0]]
    tm.assert_series_equal(result, expected)

