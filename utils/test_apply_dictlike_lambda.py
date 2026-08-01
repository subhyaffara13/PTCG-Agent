
def test_apply_dictlike_lambda(ops, by_row, expected):
    # GH53400
    ser = Series([1, 2, 3])
    result = ser.apply(ops, by_row=by_row)
    tm.assert_equal(result, expected)

