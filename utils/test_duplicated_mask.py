
def test_duplicated_mask(keep, vals):
    # GH#48150
    ser = Series([1, 2, NA, NA, NA], dtype="Int64")
    result = ser.duplicated(keep=keep)
    expected = Series([False, False, *vals])
    tm.assert_series_equal(result, expected)

