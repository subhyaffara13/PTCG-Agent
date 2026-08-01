
def test_series_reductions(op, expected):
    ser = Series([1, 2], dtype="Int64")
    result = getattr(ser, op)()
    tm.assert_equal(result, expected)

